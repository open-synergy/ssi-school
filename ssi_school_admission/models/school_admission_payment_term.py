# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolAdmissionPaymentTerm(models.Model):
    """
    Represents a payment installment term within a school admission
    record, tracking invoice status, amounts, and due dates for
    one payment period.
    """

    _name = "school_admission_payment_term"
    _description = "School Admission Payment Term"
    _order = "sequence, id"

    @api.depends(
        "invoice_id",
        "admission_id.state",
        "manually_control",
    )
    def _compute_state(self):
        for record in self:
            if record.admission_id.state in ["draft", "confirm"]:
                state = "draft"
            elif record.admission_id.state in ["open", "done"]:
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

    admission_id = fields.Many2one(
        string="Admission",
        comodel_name="school_admission",
        ondelete="cascade",
        help=("The parent school admission record this payment " "term belongs to."),
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="admission_id.student_id",
        store=True,
        help="The student partner derived from the parent admission record.",
    )
    name = fields.Char(
        string="Term",
        required=True,
        help="The name or label for this payment installment term.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help=("Determines the display order of this term " "in the admission."),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="admission_id.currency_id",
        store=True,
        required=False,
        help="The currency derived from the parent admission record.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="admission_id.pricelist_id",
        store=True,
        help="The pricelist derived from the parent admission record.",
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="school_admission_payment_term_detail",
        inverse_name="term_id",
        copy=True,
        help="The individual fee items included in this payment term.",
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="The total amount before taxes for this term.",
    )
    amount_tax = fields.Monetary(
        string="Tax",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="The total tax amount for this term.",
    )
    amount_total = fields.Monetary(
        string="Total",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="The total amount including taxes for this term.",
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.move",
        readonly=True,
        ondelete="restrict",
        help="The invoice generated for this payment term, if any.",
    )
    date_invoice = fields.Date(
        string="Estimated Invoice Date",
        help="The estimated date when the invoice will be issued.",
    )
    date_due = fields.Date(
        string="Estimated Due Date",
        help="The estimated due date for payment of this term.",
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
        help="The current state of this payment term.",
    )
    manually_control = fields.Boolean(
        string="Manually Controlled",
        default=False,
        help=(
            "Marks this term as manually controlled, " "skipping automatic invoicing."
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
        admission = self.admission_id
        partner = admission.student_id
        journal = admission.receivable_journal_id
        lines = []
        for detail in self.detail_ids:
            lines += [
                (0, 0, detail._prepare_invoice_line())
            ]  # pylint: disable=protected-access
        return {
            "date": fields.Date.today(),
            "ref": admission.name,
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "partner_id": partner.id,
            "currency_id": admission.currency_id.id,
            "invoice_user_id": False,
            "invoice_date": self.date_invoice or fields.Date.today(),
            "invoice_date_due": self.date_due
            or self.date_invoice
            or fields.Date.today(),
            "invoice_origin": admission.name,
            "invoice_payment_term_id": False,
            "invoice_line_ids": lines,
        }

    def _delete_invoice(self):
        self.ensure_one()
        invoice = self.invoice_id
        self.detail_ids.write({"invoice_line_id": False})
        self.write({"invoice_id": False})
        invoice.unlink()
