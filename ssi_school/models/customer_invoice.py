# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


# Adds a pre-cancel guard rejecting the cancellation of an invoice whose
# lines were already released by an enrollment's Revenue Recognition move
# -- see ``_45_check_no_revenue_recognition`` below -- and the
# cross-module force-delete guard ``_check_force_delete_allowed``.
class CustomerInvoice(models.Model):
    _name = "customer_invoice"
    _inherit = [
        "customer_invoice",
    ]

    def _get_recognized_enrollment_detail(self):
        """Find an enrollment detail line of this invoice already recognized.

        Shared by the pre-cancel guard and ``_check_force_delete_allowed``
        so both apply the same criterion: a
        ``school_enrollment_payment_term_detail`` whose
        ``customer_invoice_line_id`` is one of this invoice's lines and
        whose enrollment already carries a ``recognition_move_id``.

        :return: the first matching detail record, or an empty recordset
        """
        self.ensure_one()
        Detail = self.env[  # pylint: disable=invalid-name
            "school_enrollment_payment_term_detail"
        ]
        return Detail.search(
            [
                ("customer_invoice_line_id", "in", self.line_ids.ids),
                ("term_id.enrollment_id.recognition_move_id", "!=", False),
            ],
            limit=1,
        )

    def _check_force_delete_allowed(self):
        """Reject a force delete of an invoice another document relies on.

        Cross-module hook (contract K1) called by the Force Delete
        Invoice flow of a payment term before anything is changed.
        Read-only: it must never write. Every override MUST call
        ``super()`` first and raise a ``UserError`` in the
        Context/Database ID/Problem/Solution format naming the blocking
        document's ``display_name``. The base implementation rejects an
        invoice whose line was already released by an enrollment's
        Revenue Recognition, whatever the invoice state.

        :raises UserError: when one of this invoice's lines is
            referenced by a recognized enrollment payment term detail
        :return: None
        """
        self.ensure_one()
        recognized_detail = self._get_recognized_enrollment_detail()
        if recognized_detail:
            enrollment = recognized_detail.term_id.enrollment_id
            error_message = (
                _(
                    """
Context: Force delete customer invoice
Database ID: %s
Problem: Line '%s' was already released by the Revenue Recognition of enrollment '%s'
Solution: Revenue Recognition entries cannot be undone by deleting this invoice
"""
                )
                % (
                    self.id,
                    recognized_detail.name,
                    enrollment.display_name,
                )
            )
            raise UserError(error_message)

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
        recognized_detail = self._get_recognized_enrollment_detail()
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
