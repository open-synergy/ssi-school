# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SchoolAdmission(models.Model):
    """
    Adds the ability to export the unpaid customer invoices generated
    from this admission's payment terms into a
    ``customer_invoice_export`` document, via a dedicated wizard.
    """

    _name = "school_admission"
    _inherit = [
        "school_admission",
    ]

    create_invoice_export_ok = fields.Boolean(
        string="Can Create Invoice Export",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether the unpaid invoices "
            "generated from this admission's payment terms may be "
            "exported via the Create Invoice Export wizard."
        ),
    )

    def _get_exportable_move(self):
        """Return the ``account.move`` of this admission's unpaid invoices.

        Only payment terms whose ``customer_invoice_id`` is set, in the
        "Unpaid" (``open``) state, and whose invoice already carries a
        posted journal entry (``move_id``) are considered. Terms without
        an invoice yet, or whose invoice is still ``draft``/``confirm``
        or already ``done`` (Paid), contribute no move.

        :return: an ``account.move`` recordset
        """
        self.ensure_one()
        exportable_terms = self.payment_term_ids.filtered(
            lambda term: term.customer_invoice_id
            and term.customer_invoice_id.state == "open"
            and term.customer_invoice_id.move_id
        )
        return exportable_terms.mapped("customer_invoice_id.move_id")

    def _check_create_invoice_export_policy(self):
        """Ensure this admission is allowed to export invoices.

        Respects the ``bypass_policy_check`` context, mirroring
        ``_check_create_invoice_policy``.

        :raises UserError: when ``create_invoice_export_ok`` is False
        :return: True when the policy allows it
        """
        self.ensure_one()
        if self.env.context.get("bypass_policy_check", False):
            return True
        if not self.create_invoice_export_ok:
            error_message = (
                _(
                    """
Context: Create invoice export
Database ID: %s
Problem: Document is not allowed to create invoice export
Solution: Check create invoice export policy prerequisite
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)
        return True

    def action_open_create_invoice_export_wizard(self):
        """Open the wizard to export unpaid invoices of this admission.

        :return: an ``ir.actions.act_window`` opening the wizard
        """
        for record in self.sudo():
            # pylint: disable=protected-access
            result = record._open_create_invoice_export_wizard()
        return result

    def _open_create_invoice_export_wizard(self):
        """Build the action opening the Create Invoice Export wizard.

        Passes this admission via the
        ``active_model``/``active_id``/``active_ids`` context, mirroring
        ``_open_create_due_invoice_wizard``.

        :return: an ``ir.actions.act_window`` dict
        """
        self.ensure_one()
        waction = self.env.ref(
            "ssi_school_admission_customer_invoice_export."
            "school_admission_wizard_create_invoice_export_action"
        ).read()[0]
        waction.update(
            {
                "context": {
                    "active_model": "school_admission",
                    "active_id": self.id,
                    "active_ids": [self.id],
                },
            }
        )
        return waction

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        res.append("create_invoice_export_ok")
        return res
