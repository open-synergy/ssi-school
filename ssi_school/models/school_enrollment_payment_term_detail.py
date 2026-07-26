# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

ADDENDUM_LOCK_ALLOWED_FIELDS = {"customer_invoice_line_id", "locked", "sequence"}


class SchoolEnrollmentPaymentTermDetail(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a product/fee line detail on an actual enrollment payment term.
    Inherits mixin.product_line_account which provides standard product line fields
    such as name, account_id, uom_id, uom_quantity, price_unit, tax_ids,
    price_subtotal, price_tax, and price_total. If the term is linked to a customer
    invoice, each detail line will reference the corresponding customer invoice line
    (customer_invoice_line_id) created when the customer invoice is generated.
    """

    _name = "school_enrollment_payment_term_detail"
    _description = "School Enrollment Payment Term Detail"
    _order = "sequence, product_category_id, product_id, id"
    _inherit = [
        "mixin.product_line_account",
        "mixin.many2one_configurator",
    ]

    term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_enrollment_payment_term",
        ondelete="cascade",
        help="The enrollment payment term that owns this fee line.",
    )
    product_id = fields.Many2one(required=True)
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="term_id.enrollment_id.currency_id",
        store=True,
        required=False,
        help="The billing currency, automatically taken from the enrollment.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="term_id.enrollment_id.pricelist_id",
        store=True,
        help="The pricelist used, automatically taken from the enrollment.",
    )
    customer_invoice_line_id = fields.Many2one(
        string="Customer Invoice Line",
        comodel_name="customer_invoice.line",
        readonly=True,
        ondelete="restrict",
        help=(
            "The customer invoice line linked to this detail, "
            "automatically populated when the customer invoice is generated."
        ),
    )
    allowed_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Allowed Products",
        compute="_compute_allowed_product_ids",
        store=False,
        compute_sudo=True,
        help="Products allowed on this line, per the enrollment's payment template.",
    )
    addendum_ok = fields.Boolean(
        string="Can Addendum",
        related="term_id.enrollment_id.addendum_ok",
        help=(
            "Whether the owning enrollment currently allows adding new "
            "payment terms/details via the addendum mechanism."
        ),
    )
    locked = fields.Boolean(
        string="Locked",
        default=False,
        readonly=True,
        copy=False,
        help=(
            "Automatically set to True when the enrollment is opened. "
            "Locked detail lines can no longer be edited or deleted; "
            "new detail lines added afterwards via the addendum mechanism "
            "start unlocked."
        ),
    )

    def _check_addendum_lock(self, vals):
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

    @api.depends("term_id.enrollment_id.payment_template_id")
    def _compute_allowed_product_ids(self):
        for record in self:
            result = False
            template = record.term_id.enrollment_id.payment_template_id
            if template:
                result = record._m2o_configurator_get_filter(
                    object_name="product.product",
                    method_selection=template.product_selection_method,
                    manual_recordset=template.product_ids,
                    domain=template.product_domain,
                    python_code=template.product_python_code,
                )
            record.allowed_product_ids = result

    def _prepare_invoice_line(self):
        """Build the ``customer_invoice.line`` values for this fee line.

        Extension point: override in a glue module to add extra line
        values. The link to the parent document
        (``customer_invoice_id``) is intentionally left out -- it is
        added by ``school_enrollment_payment_term._create_invoice``,
        which owns the newly created header.

        :return: dict of ``customer_invoice.line`` values
        """
        self.ensure_one()
        aa = (  # pylint: disable=invalid-name,consider-using-ternary
            self.analytic_account_id and self.analytic_account_id.id or False
        )
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

    @api.model
    def create(self, vals):
        result = super().create(vals)
        enrollment = result.term_id.enrollment_id
        if enrollment:
            enrollment._recompute_product_summaries()  # pylint: disable=protected-access
        return result

    def write(self, vals):
        self._check_addendum_lock(vals)
        result = super().write(vals)
        self.mapped(
            "term_id.enrollment_id"
        )._recompute_product_summaries()  # pylint: disable=protected-access
        return result

    def unlink(self):
        self._check_addendum_lock_unlink()
        enrollments = self.mapped("term_id.enrollment_id")
        result = super().unlink()
        enrollments._recompute_product_summaries()  # pylint: disable=protected-access
        return result
