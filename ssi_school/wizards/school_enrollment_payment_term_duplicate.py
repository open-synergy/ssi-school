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
        """Prefill the wizard from the payment term it was opened on.

        Overridden so the dialog opens already describing the copy: the
        source term becomes ``term_id`` and its header values seed ``name``
        (suffixed with "(copy)"), ``sequence``, ``date_invoice``, and
        ``date_due``.

        :param fields_list: list of field names Odoo asks defaults for
        :return: dict of default values
        """
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
        """Create the duplicated payment term and close the dialog.

        Triggered by the wizard button; the work is delegated to
        ``_duplicate_term``. A new ``school_enrollment_payment_term`` is
        created on the same enrollment as the source.

        :return: an ``ir.actions.act_window_close`` action
        """
        for record in self.sudo():
            result = record._duplicate_term()
        return result

    def _duplicate_term(self):
        """Copy the source term together with all of its detail lines.

        The copy keeps the source ``detail_ids`` but is detached from any
        invoice: ``customer_invoice_id`` comes back empty from
        ``_prepare_duplicate_defaults`` and the copied detail lines have
        their ``customer_invoice_line_id`` cleared.

        :return: an ``ir.actions.act_window_close`` action
        """
        self.ensure_one()
        new_term = self.term_id.copy(self._prepare_duplicate_defaults())
        new_term.detail_ids.write({"customer_invoice_line_id": False})
        return {"type": "ir.actions.act_window_close"}

    def _prepare_duplicate_defaults(self):
        """Build the override values passed to ``term_id.copy()``.

        Extension point: override in a glue module to carry extra header
        fields into the duplicate without touching ``_duplicate_term``.

        :return: dict of ``school_enrollment_payment_term`` values
        """
        self.ensure_one()
        return {
            "name": self.name,
            "sequence": self.sequence,
            "date_invoice": self.date_invoice,
            "date_due": self.date_due,
            "customer_invoice_id": False,
        }
