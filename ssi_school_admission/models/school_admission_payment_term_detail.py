# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

ADDENDUM_LOCK_ALLOWED_FIELDS = {"customer_invoice_line_id", "locked", "sequence"}


class SchoolAdmissionPaymentTermDetail(models.Model):
    """
    Represents a single fee line detail within a school admission
    payment term, specifying the product, amount, and associated
    customer invoice line for one payment item.
    """

    _name = "school_admission_payment_term_detail"
    _description = "School Admission Payment Term Detail"
    _order = "sequence, product_category_id, product_id, id"
    _inherit = [
        "mixin.product_line_account",
        "mixin.many2one_configurator",
    ]

    term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_admission_payment_term",
        ondelete="cascade",
        help="The parent payment term this detail line belongs to.",
    )
    product_id = fields.Many2one(required=True)
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="term_id.admission_id.currency_id",
        store=True,
        required=False,
        help="The currency derived from the parent admission record.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="term_id.admission_id.pricelist_id",
        store=True,
        help="The pricelist derived from the parent admission record.",
    )
    customer_invoice_line_id = fields.Many2one(
        string="Customer Invoice Line",
        comodel_name="customer_invoice.line",
        readonly=True,
        ondelete="restrict",
        help=(
            "The customer invoice line linked to this detail "
            "after the term is invoiced."
        ),
    )
    allowed_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Allowed Products",
        compute="_compute_allowed_product_ids",
        store=False,
        compute_sudo=True,
        help="Products allowed on this line, per the admission's payment template.",
    )

    addendum_ok = fields.Boolean(
        string="Can Addendum",
        related="term_id.admission_id.addendum_ok",
        help=(
            "Whether the owning admission currently allows adding new "
            "payment terms/details via the addendum mechanism."
        ),
    )
    locked = fields.Boolean(
        string="Locked",
        default=False,
        readonly=True,
        copy=False,
        help=(
            "Automatically set to True when the admission is opened. "
            "Locked detail lines can no longer be edited or deleted; "
            "new detail lines added afterwards via the addendum mechanism "
            "start unlocked."
        ),
    )
    voided = fields.Boolean(
        string="Voided",
        default=False,
        readonly=True,
        copy=False,
        help=(
            "Set when this line's full amount has been moved to another "
            "payment term. A voided line no longer counts toward the "
            "term total, is never billed on a customer invoice, and is "
            "excluded from product summary; it stays visible on its "
            "original term only as a trace of where the amount went. "
            "This is not a way to reduce the billed amount -- "
            "price_unit keeps its original value. Can only be set "
            "through the ORM; this module provides no button/action "
            "that enables it."
        ),
    )

    @api.depends("term_id.admission_id.payment_template_id")
    def _compute_allowed_product_ids(self):
        """List the products allowed on this payment term detail.

        Delegates to the m2o configurator of the payment template used
        by the owning admission, so the selection method, manual
        recordset, domain and python code configured there decide the
        result. Empty when the admission has no payment template.
        """
        for record in self:
            result = False
            template = record.term_id.admission_id.payment_template_id
            if template:
                result = record._m2o_configurator_get_filter(
                    object_name="product.product",
                    method_selection=template.product_selection_method,
                    manual_recordset=template.product_ids,
                    domain=template.product_domain,
                    python_code=template.product_python_code,
                )
            record.allowed_product_ids = result

    def _check_addendum_lock(self, vals):
        """Forbid editing a locked payment term detail.

        Skipped when the context flag ``bypass_addendum_lock`` is set,
        or when the write only touches the fields listed in
        ``ADDENDUM_LOCK_ALLOWED_FIELDS``.

        :param vals: the write values about to be applied
        :return: ``None``
        :raises UserError: when a locked detail would be modified
        """
        if self.env.context.get("bypass_addendum_lock"):
            return
        if set(vals.keys()) <= ADDENDUM_LOCK_ALLOWED_FIELDS:
            return
        for record in self:
            if record.locked:
                error_message = (
                    _(
                        """
Context: Update payment term detail
Database ID: %s
Problem: Payment term detail '%s' is locked and cannot be modified
Solution: Add a new detail line via the addendum mechanism instead of editing this one
"""
                    )
                    % (record.id, record.name)
                )
                raise UserError(error_message)

    def _check_addendum_lock_unlink(self):
        """Forbid deleting a locked payment term detail.

        Skipped when the context flag ``bypass_addendum_lock`` is set.

        :return: ``None``
        :raises UserError: when a locked detail would be deleted
        """
        if self.env.context.get("bypass_addendum_lock"):
            return
        for record in self:
            if record.locked:
                error_message = (
                    _(
                        """
Context: Delete payment term detail
Database ID: %s
Problem: Payment term detail '%s' is locked and cannot be deleted
Solution: Locked detail lines are permanent; create a new one via the addendum mechanism
"""
                    )
                    % (record.id, record.name)
                )
                raise UserError(error_message)

    @api.model
    def create(self, vals):
        """Create the detail and refresh the admission product summary.

        Overridden so the aggregated ``product_summary_ids`` of the
        owning admission stays in sync with its term details.

        :param vals: values of the detail to create
        :return: the created record
        """
        record = super().create(vals)
        admission = record.term_id.admission_id
        if admission:
            admission._recompute_product_summary()  # pylint: disable=protected-access
        return record

    def write(self, vals):
        """Write the detail, enforcing the addendum lock first.

        Overridden both to reject edits on locked details and to
        refresh the aggregated product summary of the owning admission.

        :param vals: values to write
        :return: ``True``
        :raises UserError: when a locked detail would be modified
        """
        self._check_addendum_lock(vals)
        result = super().write(vals)
        self.mapped(
            "term_id.admission_id"
        )._recompute_product_summary()  # pylint: disable=protected-access
        return result

    def unlink(self):
        """Delete the detail, enforcing the addendum lock first.

        Overridden both to reject deletion of locked details and to
        refresh the aggregated product summary of the owning admission.

        :return: ``True``
        :raises UserError: when a locked detail would be deleted
        """
        self._check_addendum_lock_unlink()
        admissions = self.mapped("term_id.admission_id")
        result = super().unlink()
        admissions._recompute_product_summary()  # pylint: disable=protected-access
        return result

    def _prepare_invoice_line(self):
        """Build the ``customer_invoice.line`` values for this fee line.

        Extension point: override in a glue module to add extra line
        values. The link to the parent document
        (``customer_invoice_id``) is intentionally left out -- it is
        added by ``school_admission_payment_term._create_invoice``,
        which owns the newly created header.

        :return: dict of ``customer_invoice.line`` values
        """
        self.ensure_one()
        aa = (
            self.analytic_account_id and self.analytic_account_id.id or False
        )  # pylint: disable=invalid-name,consider-using-ternary
        return {
            "product_id": self.product_id.id,
            "name": self.name,
            "account_id": self.account_id.id,
            "uom_id": self.uom_id.id,
            "uom_quantity": self.uom_quantity,
            "price_unit": self.price_unit,
            "tax_ids": [(6, 0, self.tax_ids.ids)],
            "analytic_account_id": aa or False,
        }
