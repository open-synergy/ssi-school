# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

ADDENDUM_LOCK_ALLOWED_FIELDS = {
    "customer_invoice_line_id",
    "locked",
    "sequence",
    "final_usage_id",
    "final_account_id",
}
# Writable on a locked detail only while it is not yet invoiced -- see
# ``_check_addendum_lock``. Once ``customer_invoice_line_id`` is set the
# amount is already billed on that account, so classification can no
# longer change without desynchronizing the customer invoice line.
CONDITIONAL_LOCK_ALLOWED_FIELDS = {"usage_id", "account_id"}


class SchoolEnrollmentPaymentTermDetail(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a product/fee line detail on an actual enrollment payment
    term. Inherits mixin.product_line_account which provides standard
    product line fields such as name, account_id, uom_id, uom_quantity,
    price_unit, tax_ids, price_subtotal, price_tax, and price_total. If
    the term is linked to a customer invoice, each detail line will
    reference the corresponding customer invoice line
    (customer_invoice_line_id) created when the customer invoice is
    generated.
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
    final_usage_id = fields.Many2one(
        string="Final Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
        help=(
            "Usage used to auto-fill Final Account from the product's "
            "account configuration."
        ),
    )
    final_account_id = fields.Many2one(
        string="Final Account",
        comodel_name="account.account",
        ondelete="restrict",
        help=(
            "Revenue account this line is recognized to once the "
            "enrollment finishes and Revenue Recognition posts, "
            "auto-filled from the product's account configuration for "
            "Final Usage. Left empty, this line is never recognized -- "
            "e.g. a deposit/holding fee."
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
    voided = fields.Boolean(
        string="Voided",
        default=False,
        readonly=True,
        copy=False,
        help=(
            "Set when this line's full amount has been moved to another "
            "payment term. A voided line no longer counts toward the "
            "term total, is never billed on a customer invoice, and is "
            "excluded from product summary and fee analysis; it stays "
            "visible on its original term only as a trace of where the "
            "amount went. This is not a way to reduce the billed amount "
            "-- price_unit keeps its original value. Can only be set "
            "through the ORM; this module provides no button/action "
            "that enables it."
        ),
    )

    def _check_addendum_lock(self, vals):
        """Reject writes on a locked payment term detail.

        Guard called from ``write``. The write passes when the context
        carries ``bypass_addendum_lock``, or when every key of ``vals``
        belongs to ``ADDENDUM_LOCK_ALLOWED_FIELDS``
        (``customer_invoice_line_id``, ``locked``, ``sequence``,
        ``final_usage_id``, ``final_account_id``) -- the bookkeeping and
        revenue-classification fields that stay writable even after
        locking. ``CONDITIONAL_LOCK_ALLOWED_FIELDS`` (``usage_id``,
        ``account_id``) is a second, narrower exception: writable on a
        locked record only while its own ``customer_invoice_line_id``
        is still empty, rejected once that record is invoiced. Every
        other field stays permanently locked, and a new line has to be
        added through the addendum mechanism instead.

        :param vals: write values whose keys are checked against the
            allowed field sets
        :raises UserError: when a locked detail line is written with a
            field outside the allowed sets, or with a conditional
            field while already invoiced
        :return: None
        """
        if self.env.context.get("bypass_addendum_lock"):
            return
        extra_keys = set(vals.keys()) - ADDENDUM_LOCK_ALLOWED_FIELDS
        if not extra_keys:
            return
        blocking_keys = extra_keys - CONDITIONAL_LOCK_ALLOWED_FIELDS
        conditional_keys = extra_keys & CONDITIONAL_LOCK_ALLOWED_FIELDS
        for record in self:
            if not record.locked:
                continue
            if blocking_keys or (conditional_keys and record.customer_invoice_line_id):
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
        """Reject deletion of a locked payment term detail.

        Guard called from ``unlink``. Deletion only passes when the
        context carries ``bypass_addendum_lock``; a locked detail line
        is permanent because it may already be reflected in a customer
        invoice line, so a correction has to be booked as a new
        addendum line.

        :raises UserError: when a locked detail line is deleted
        :return: None
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

    @api.depends("term_id.enrollment_id.payment_template_id")
    def _compute_allowed_product_ids(self):
        """Compute the products selectable on this fee line.

        Resolves the Product Configuration of the payment template of
        the owning enrollment
        (``term_id.enrollment_id.payment_template_id``) through
        ``_m2o_configurator_get_filter``, honouring its selection
        method, manual product list, domain, or python code. When the
        enrollment has no payment template the field is left empty.

        :return: None
        """
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

    @api.onchange("product_id", "final_usage_id")
    def onchange_final_account_id(self):
        """Auto-fill ``final_account_id`` from the product's usage account.

        Resolves ``product_id._get_product_account`` for
        ``final_usage_id.code``; a product/usage combination without a
        matching account configuration leaves ``final_account_id``
        empty rather than raising, so the line stays valid and simply
        never gets recognized.

        :return: None
        """
        self.final_account_id = False
        if self.product_id and self.final_usage_id:
            self.final_account_id = self.product_id._get_product_account(
                usage_code=self.final_usage_id.code
            )

    def _prepare_invoice_line(self):
        """Build the ``customer_invoice.line`` values for this fee line.

        Extension point: override in a glue module to add extra line
        values. The link to the parent document
        (``customer_invoice_id``) is intentionally left out -- it is
        added by ``school_enrollment_payment_term._create_invoice``,
        which owns the newly created header. When the owning
        enrollment already finished (``done``) with Revenue
        Recognition enabled and this line carries a Final Account, a
        due invoice created after the fact bills straight to that
        Final Account instead of the line's own temporary account --
        there is no later Revenue Recognition move to reclass it.

        :return: dict of ``customer_invoice.line`` values
        """
        self.ensure_one()
        aa = (  # pylint: disable=invalid-name,consider-using-ternary
            self.analytic_account_id and self.analytic_account_id.id or False
        )
        enrollment = self.term_id.enrollment_id
        account = self.account_id
        if (
            enrollment.state == "done"
            and enrollment.revenue_recognition
            and self.final_account_id
        ):
            account = self.final_account_id
        return {
            "product_id": self.product_id.id,
            "name": self.name,
            "account_id": account.id,
            "uom_id": self.uom_id.id,
            "uom_quantity": self.uom_quantity,
            "price_unit": self.price_unit,
            "tax_ids": [(6, 0, self.tax_ids.ids)],
            "analytic_account_id": aa or False,
        }

    @api.model
    def create(self, vals):
        """Refresh the enrollment payment summary after creation.

        Overridden so that a detail line created outside the
        enrollment form -- by the payment template computation or the
        duplicate wizard -- still triggers
        ``_recompute_product_summaries`` on the enrollment of its
        term, keeping ``product_summary_ids`` in step with the fee
        lines.

        :param vals: values of the payment term detail to create
        :return: created ``school_enrollment_payment_term_detail``
            record
        """
        result = super().create(vals)
        enrollment = result.term_id.enrollment_id
        if enrollment:
            enrollment._recompute_product_summaries()  # pylint: disable=protected-access
        return result

    def write(self, vals):
        """Enforce the addendum lock and refresh the payment summary.

        Overridden to run ``_check_addendum_lock`` before the write, so
        locked detail lines cannot be modified, and to recompute
        ``product_summary_ids`` on every touched enrollment afterwards.

        :param vals: values to write
        :raises UserError: when a locked detail line is written with a
            field outside ``ADDENDUM_LOCK_ALLOWED_FIELDS``
        :return: ``True``
        """
        self._check_addendum_lock(vals)
        result = super().write(vals)
        self.mapped(
            "term_id.enrollment_id"
        )._recompute_product_summaries()  # pylint: disable=protected-access
        return result

    def unlink(self):
        """Enforce the addendum lock and refresh the payment summary.

        Overridden to run ``_check_addendum_lock_unlink`` before the
        deletion, so locked detail lines cannot be removed, and to
        recompute ``product_summary_ids`` on the enrollments collected
        before the records disappear.

        :raises UserError: when a locked detail line is deleted
        :return: ``True``
        """
        self._check_addendum_lock_unlink()
        enrollments = self.mapped("term_id.enrollment_id")
        result = super().unlink()
        enrollments._recompute_product_summaries()  # pylint: disable=protected-access
        return result
