# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SchoolEnrollmentPaymentTermWizardDuplicate(models.TransientModel):
    """
    Wizard that duplicates a school_enrollment_payment_term record.
    Copies every detail line (detail_ids) from the source term to a new term
    on the same enrollment, while only the header fields (name, sequence,
    date_invoice, date_due) are taken from the wizard input.
    """

    _name = "school_enrollment_payment_term.wizard_duplicate"
    _description = "Duplicate School Enrollment Payment Term"

    term_id = fields.Many2one(
        string="Source Term",
        comodel_name="school_enrollment_payment_term",
        required=True,
        readonly=True,
        help="The payment term whose detail lines will be copied to the new term.",
    )
    name = fields.Char(
        string="Term Name",
        required=True,
        help="Name of the new payment term to be created.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help=(
            "Order of the new payment term within the enrollment. "
            "Lower values appear first."
        ),
    )
    date_invoice = fields.Date(
        string="Estimated Invoice Date",
        help="Estimated date for issuing the invoice for the new payment term.",
    )
    date_due = fields.Date(
        string="Estimated Due Date",
        help="Estimated due date for payment of the new payment term.",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get("active_id")
        if active_id:
            term = self.env["school_enrollment_payment_term"].browse(active_id)
            res["term_id"] = term.id
            res["name"] = _("%s (copy)") % term.name
            res["sequence"] = term.sequence
            res["date_invoice"] = term.date_invoice
            res["date_due"] = term.date_due
        return res

    def action_duplicate(self):
        for record in self.sudo():
            result = record._duplicate_term()
        return result

    def _duplicate_term(self):
        self.ensure_one()
        new_term = self.term_id.copy(self._prepare_duplicate_defaults())
        new_term.detail_ids.write({"invoice_line_id": False})
        return {"type": "ir.actions.act_window_close"}

    def _prepare_duplicate_defaults(self):
        self.ensure_one()
        return {
            "name": self.name,
            "sequence": self.sequence,
            "date_invoice": self.date_invoice,
            "date_due": self.date_due,
            "invoice_id": False,
        }
