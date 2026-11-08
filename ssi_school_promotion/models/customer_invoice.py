# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


# Adds the promotion code usage allocation rule to the cross-module
# force-delete guard ``_check_force_delete_allowed`` (contract K1 of
# ``ssi_school``).
class CustomerInvoice(models.Model):
    _name = "customer_invoice"
    _inherit = [
        "customer_invoice",
    ]

    def _check_force_delete_allowed(self):
        """Reject a force delete of an invoice a usage allocation uses.

        Extends the K1 guard of ``ssi_school``: calls ``super()`` first,
        then rejects the invoice when any
        ``promotion_code_usage_allocation`` points to its receivable
        journal item, whatever the state of the usage document, because
        the ``ondelete="restrict"`` reference would still block the
        delete. Skipped when the invoice has no receivable journal item.
        Read-only: it never writes.

        :raises UserError: when a promotion code usage allocation
            references the receivable journal item of this invoice
        :return: None
        """
        super()._check_force_delete_allowed()
        self.ensure_one()
        move_line = self.receivable_move_line_id
        if not move_line:
            return
        allocation = (
            self.env["promotion_code_usage_allocation"]
            .sudo()
            .search(
                [("move_line_id", "=", move_line.id)],
                limit=1,
            )
        )
        if allocation:
            error_message = (
                _(
                    """
Context: Force delete customer invoice
Database ID: %s
Problem: Invoice is referenced by promotion code usage allocation '%s' of usage '%s'
Solution: Remove the allocation from the promotion code usage document first
"""
                )
                % (
                    self.id,
                    allocation.display_name,
                    allocation.usage_id.display_name,
                )
            )
            raise UserError(error_message)
