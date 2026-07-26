# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

ADDENDUM_LOCK_ALLOWED_FIELDS = {
    "customer_invoice_id",
    "manually_control",
    "locked",
    "sequence",
}


class SchoolEnrollmentPaymentTerm(models.Model):
    """
    Represents an actual payment billing term on a specific enrollment.
    SchoolEnrollmentPaymentTerm is a realized instance of a template term applied
    to a specific enrollment. Each term can generate one customer invoice
    (customer_invoice_id) via action_create_invoice. The state is automatically
    computed: draft (enrollment in draft/confirm), uninvoiced (enrollment
    open/done, no customer invoice yet), invoiced (customer invoice created),
    manual (manually controlled), cancelled (enrollment cancelled).
    Totals (amount_untaxed, amount_tax, amount_total) are computed from detail_ids.
    """

    _name = "school_enrollment_payment_term"
    _description = "School Enrollment Payment Term"
    _order = "sequence, id"

    @api.depends(
        "customer_invoice_id",
        "enrollment_id.state",
        "manually_control",
    )
    def _compute_state(self):
        for record in self:
            if record.enrollment_id.state in ["draft", "confirm"]:
                state = "draft"
            elif record.enrollment_id.state in ["open", "done"]:
                if record.customer_invoice_id:
                    state = "invoiced"
                elif record.manually_control:
                    state = "manual"
                else:
                    state = "uninvoiced"
            else:
                state = "cancelled"
            record.state = state

    @api.depends(
        "detail_ids",
        "detail_ids.price_subtotal",
        "detail_ids.price_tax",
        "detail_ids.price_total",
    )
    def _compute_total(self):
        for record in self:
            amount_untaxed = amount_tax = amount_total = 0.0
            for detail in record.detail_ids:
                amount_untaxed += detail.price_subtotal
                amount_tax += detail.price_tax
                amount_total += detail.price_total
            record.amount_untaxed = amount_untaxed
            record.amount_tax = amount_tax
            record.amount_total = amount_total

    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        ondelete="cascade",
        help="The enrollment that owns this payment term.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="enrollment_id.student_id.contact_id",
        store=True,
        help=(
            "The student's contact partner, automatically "
            "populated from the enrollment."
        ),
    )
    name = fields.Char(
        string="Term",
        required=True,
        help=(
            "Name of the payment period, "
            "e.g. 'Registration Fee' or 'Monthly Tuition'."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help=(
            "Order of the payment period within the enrollment. "
            "Lower values appear first."
        ),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="enrollment_id.currency_id",
        store=True,
        required=False,
        help="The billing currency, automatically taken from the enrollment.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="enrollment_id.pricelist_id",
        store=True,
        help="The pricelist used, automatically taken from the enrollment.",
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="school_enrollment_payment_term_detail",
        inverse_name="term_id",
        copy=True,
        help="Product/fee detail lines within this payment period.",
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help=(
            "Total billing amount before tax, "
            "automatically computed from the detail lines."
        ),
    )
    amount_tax = fields.Monetary(
        string="Tax",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="Total tax amount, automatically computed from the detail lines.",
    )
    amount_total = fields.Monetary(
        string="Total",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help=(
            "Total billing amount including tax, "
            "automatically computed from the detail lines."
        ),
    )
    customer_invoice_id = fields.Many2one(
        string="# Customer Invoice",
        comodel_name="customer_invoice",
        readonly=True,
        ondelete="restrict",
        help="The customer invoice linked to this payment period.",
    )
    date_invoice = fields.Date(
        string="Estimated Invoice Date",
        help="Estimated date for issuing the invoice for this billing period.",
    )
    date_due = fields.Date(
        string="Estimated Due Date",
        help="Estimated due date for payment of this billing period.",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("uninvoiced", "Uninvoiced"),
            ("invoiced", "Invoiced"),
            ("manual", "Manually Controlled"),
            ("cancelled", "Cancelled"),
        ],
        compute="_compute_state",
        store=True,
        help=(
            "Billing status: "
            "Draft = enrollment still in draft/confirm, "
            "Uninvoiced = enrollment open/done but no customer invoice yet, "
            "Invoiced = customer invoice created, "
            "Manually Controlled = managed manually, "
            "Cancelled = enrollment cancelled."
        ),
    )
    manually_control = fields.Boolean(
        string="Manually Controlled",
        default=False,
        help=(
            "If enabled, this billing term is managed manually "
            "and does not require a customer invoice."
        ),
    )
    enrollment_state = fields.Selection(
        string="Enrollment State",
        related="enrollment_id.state",
        store=True,
        help=(
            "Status of the owning enrollment, used to control "
            "term-level actions such as duplication."
        ),
    )
    addendum_ok = fields.Boolean(
        string="Can Addendum",
        related="enrollment_id.addendum_ok",
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
            "Locked payment terms can no longer be edited or deleted; "
            "new terms added afterwards via the addendum mechanism start "
            "unlocked."
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
Context: Update payment term
Database ID: %s
Problem: Payment term '%s' is locked and cannot be modified
Solution: Add a new payment term via the addendum mechanism instead of editing this one
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
Context: Delete payment term
Database ID: %s
Problem: Payment term '%s' is locked and cannot be deleted
Solution: Locked payment terms are permanent; create a new one via addendum instead
"""
                    )
                    % (record.id, record.name)
                )
                raise UserError(error_message)

    def action_create_invoice(self):
        for record in self.sudo():
            record._create_invoice()  # pylint: disable=protected-access

    def action_delete_invoice(self):
        for record in self.sudo():
            record._delete_invoice()  # pylint: disable=protected-access

    def action_disconnect_invoice(self):
        for record in self.sudo():
            record._disconnect_invoice()  # pylint: disable=protected-access

    def action_mark_as_manual(self):
        for record in self.sudo():
            record._mark_as_manual()  # pylint: disable=protected-access

    def action_unmark_as_manual(self):
        for record in self.sudo():
            record._unmark_as_manual()  # pylint: disable=protected-access

    def action_open_duplicate_wizard(self):
        for record in self.sudo():
            result = record._open_duplicate_wizard()
        return result

    def _open_duplicate_wizard(self):
        self.ensure_one()
        waction = self.env.ref(
            "ssi_school.school_enrollment_payment_term_action_duplicate"
        ).read()[0]
        waction.update({"context": {"active_id": self.id}})
        return waction

    def _mark_as_manual(self):
        self.ensure_one()
        self.write({"manually_control": True})

    def _unmark_as_manual(self):
        self.ensure_one()
        self.write({"manually_control": False})

    def _create_invoice(self):
        """Create the ``customer_invoice`` document for this term.

        Creates the header first, then one ``customer_invoice.line`` per
        detail line, writing the resulting line back onto the detail it
        originates from, and finally links the document to this term.
        Taxes are not computed here: ``customer_invoice`` recomputes them
        itself on pre-confirm. When the enrollment has
        ``auto_confirm_customer_invoice`` enabled, the new document is
        confirmed right away.

        :return: None
        """
        self.ensure_one()
        line_model = self.env["customer_invoice.line"]
        invoice = self.env["customer_invoice"].create(self._prepare_invoice_data())
        for detail in self.detail_ids:
            # pylint: disable=protected-access
            line_data = detail._prepare_invoice_line()
            line_data["customer_invoice_id"] = invoice.id
            line = line_model.create(line_data)
            detail.write({"customer_invoice_line_id": line.id})
        self.write({"customer_invoice_id": invoice.id})
        if self.enrollment_id.auto_confirm_customer_invoice:
            invoice.action_confirm()

    def _disconnect_invoice(self):
        """Detach the customer invoice from this term without deleting it.

        Only ``customer_invoice_id`` is cleared, so the term falls back to
        the uninvoiced state while the ``customer_invoice`` document itself
        is kept.

        :return: None
        """
        self.ensure_one()
        self.write({"customer_invoice_id": False})

    def _prepare_invoice_data(self):
        """Build the ``customer_invoice`` header values for this term.

        Extension point: override in a glue module (Operating Unit, for
        instance) to add extra header values without touching
        ``_create_invoice``. Detail lines are deliberately excluded --
        they are created one by one by ``_create_invoice`` so that each
        line can be written back to its originating detail.

        :return: dict of ``customer_invoice`` values
        """
        self.ensure_one()
        enrollment = self.enrollment_id
        date = self.date_invoice or fields.Date.today()
        return {
            "type_id": enrollment.customer_invoice_type_id.id,
            "partner_id": enrollment.student_id.contact_id.id,
            "currency_id": enrollment.currency_id.id,
            "pricelist_id": enrollment.pricelist_id.id,
            "journal_id": enrollment.receivable_journal_id.id,
            "receivable_account_id": enrollment.receivable_account_id.id,
            "date": date,
            "date_due": self.date_due or date,
            "customer_document_number": enrollment.name,
        }

    def _delete_invoice(self):
        """Delete the customer invoice document created from this term.

        Only a document still in ``draft`` may be deleted. Every detail
        line is unlinked from its ``customer_invoice.line`` first, then the
        term is detached, and finally the document is deleted (its lines
        are removed by cascade).

        :raises UserError: when the customer invoice is no longer draft
        :return: None
        """
        self.ensure_one()
        invoice = self.customer_invoice_id
        if invoice.state != "draft":
            error_message = (
                _(
                    """
Context: Delete customer invoice of payment term
Database ID: %s
Problem: Customer invoice '%s' is not draft anymore and cannot be deleted
Solution: Use Disconnect Invoice to detach it from the payment term instead
"""
                )
                % (self.id, invoice.display_name)
            )
            raise UserError(error_message)
        self.detail_ids.write({"customer_invoice_line_id": False})
        self.write({"customer_invoice_id": False})
        invoice.unlink()

    @api.model
    def create(self, vals):
        result = super().create(vals)
        if result.enrollment_id:
            enrollment = result.enrollment_id
            enrollment._recompute_product_summaries()  # pylint: disable=protected-access
        return result

    def write(self, vals):
        self._check_addendum_lock(vals)
        result = super().write(vals)
        self.mapped(
            "enrollment_id"
        )._recompute_product_summaries()  # pylint: disable=protected-access
        return result

    def unlink(self):
        self._check_addendum_lock_unlink()
        enrollments = self.mapped("enrollment_id")
        result = super().unlink()
        enrollments._recompute_product_summaries()  # pylint: disable=protected-access
        return result
