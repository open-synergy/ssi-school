# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolEnrollmentPaymentTerm(models.Model):
    """
    Represents an actual payment billing term on a specific enrollment.
    SchoolEnrollmentPaymentTerm is a realized instance of a template term applied
    to a specific enrollment. Each term can generate one invoice (invoice_id) via
    action_create_invoice. The state is automatically computed: draft (enrollment
    in draft/confirm), uninvoiced (enrollment open/done, no invoice yet), invoiced
    (invoice created), manual (manually controlled), cancelled (enrollment cancelled).
    Totals (amount_untaxed, amount_tax, amount_total) are computed from detail_ids.
    """

    _name = "school_enrollment_payment_term"
    _description = "School Enrollment Payment Term"
    _order = "sequence, id"

    @api.depends(
        "invoice_id",
        "enrollment_id.state",
        "manually_control",
    )
    def _compute_state(self):
        for record in self:
            if record.enrollment_id.state in ["draft", "confirm"]:
                state = "draft"
            elif record.enrollment_id.state in ["open", "done"]:
                if record.invoice_id:
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
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.move",
        readonly=True,
        ondelete="restrict",
        help="The invoice linked to this payment period.",
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
            "Uninvoiced = enrollment open/done but no invoice yet, "
            "Invoiced = invoice created, "
            "Manually Controlled = managed manually, "
            "Cancelled = enrollment cancelled."
        ),
    )
    manually_control = fields.Boolean(
        string="Manually Controlled",
        default=False,
        help=(
            "If enabled, this billing term is managed manually "
            "and does not require an invoice."
        ),
    )

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

    def _mark_as_manual(self):
        self.ensure_one()
        self.write({"manually_control": True})

    def _unmark_as_manual(self):
        self.ensure_one()
        self.write({"manually_control": False})

    def _create_invoice(self):
        self.ensure_one()
        invoice = self.env["account.move"].create(self._prepare_invoice_data())
        self.write({"invoice_id": invoice.id})

    def _disconnect_invoice(self):
        self.ensure_one()
        self.write({"invoice_id": False})

    def _prepare_invoice_data(self):
        self.ensure_one()
        enrollment = self.enrollment_id
        partner = enrollment.student_id.contact_id
        journal = enrollment.receivable_journal_id
        lines = []
        for detail in self.detail_ids:
            lines += [
                (
                    0,
                    0,
                    detail._prepare_invoice_line(),  # pylint: disable=protected-access
                )
            ]
        return {
            "date": fields.Date.today(),
            "ref": enrollment.name,
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "partner_id": partner.id,
            "currency_id": enrollment.currency_id.id,
            "invoice_user_id": False,
            "invoice_date": self.date_invoice or fields.Date.today(),
            "invoice_date_due": self.date_due
            or self.date_invoice
            or fields.Date.today(),
            "invoice_origin": enrollment.name,
            "invoice_payment_term_id": False,
            "invoice_line_ids": lines,
        }

    def _delete_invoice(self):
        self.ensure_one()
        invoice = self.invoice_id
        self.detail_ids.write({"invoice_line_id": False})
        self.write({"invoice_id": False})
        invoice.unlink()

    @api.model
    def create(self, vals):
        result = super().create(vals)
        if result.enrollment_id:
            enrollment = result.enrollment_id
            enrollment._recompute_product_summaries()  # pylint: disable=protected-access
        return result

    def write(self, vals):
        result = super().write(vals)
        self.mapped(
            "enrollment_id"
        )._recompute_product_summaries()  # pylint: disable=protected-access
        return result

    def unlink(self):
        enrollments = self.mapped("enrollment_id")
        result = super().unlink()
        enrollments._recompute_product_summaries()  # pylint: disable=protected-access
        return result
