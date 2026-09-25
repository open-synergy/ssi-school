# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


# Adds a pre-cancel guard rejecting the cancellation of an invoice whose
# lines were already released by an enrollment's Revenue Recognition move
# -- see ``_45_check_no_revenue_recognition`` below.
class CustomerInvoice(models.Model):
    _name = "customer_invoice"
    _inherit = [
        "customer_invoice",
    ]

    # I. Pre-cancel Hook: Reject Cancellation of a Recognized Invoice
    @ssi_decorator.pre_cancel_check()
    def _45_check_no_revenue_recognition(self):
        """Reject the cancellation of an invoice already recognized.

        Runs on the ``pre_cancel_check`` slot, i.e. before this
        document leaves its current state for ``cancel``. Cancelling
        an enrollment payment term detail's customer invoice line
        after the owning enrollment's Revenue Recognition move has
        already been posted would leave that move's debit side
        pointing at a journal item that no longer exists, so any line
        already referenced by a recognized detail forbids cancelling.

        :raises UserError: when one of this invoice's own lines is
            referenced by a ``school_enrollment_payment_term_detail``
            whose enrollment already has a ``recognition_move_id``
        :return: None
        """
        self.ensure_one()
        Detail = self.env[  # pylint: disable=invalid-name
            "school_enrollment_payment_term_detail"
        ]
        recognized_detail = Detail.search(
            [
                ("customer_invoice_line_id", "in", self.line_ids.ids),
                ("term_id.enrollment_id.recognition_move_id", "!=", False),
            ],
            limit=1,
        )
        if recognized_detail:
            error_message = (
                _(
                    """
Context: Cancel customer invoice
Database ID: %s
Problem: Line '%s' was already released by the Revenue Recognition of enrollment '%s'
Solution: Revenue Recognition entries cannot be undone by cancelling this invoice
"""
                )
                % (
                    self.id,
                    recognized_detail.name,
                    recognized_detail.term_id.enrollment_id.name,
                )
            )
            raise UserError(error_message)
