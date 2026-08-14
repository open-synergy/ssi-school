# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolEnrollmentPaymentTerm(models.Model):
    """
    Lets a promotion code be redeemed directly against one enrollment
    payment term.

    Carries ``mixin.promotion_object`` so each payment term line
    tracks its own Promotion Code Usages and exposes its own eligible
    receivable journal item to ``action_populate_allocation``. Billing
    granularity for promotions is per payment term, not per
    enrollment: ``_promotion_move_line_field_name`` follows
    ``customer_invoice_id`` -- the invoice this term itself issued via
    ``action_create_invoice`` -- down to that invoice's own
    ``receivable_move_line_id``, and ``_promotion_partner_id_field_name``
    reuses this term's own ``partner_id`` (the student's contact,
    already related from ``enrollment_id.student_id.contact_id``).
    Neither attribute needs an override: both targets are plain field
    paths already present on this model and on ``customer_invoice``.
    """

    _name = "school_enrollment_payment_term"
    _inherit = [
        "school_enrollment_payment_term",
        "mixin.promotion_object",
    ]

    _promotion_move_line_field_name = "customer_invoice_id.receivable_move_line_id"
    _promotion_partner_id_field_name = "partner_id"
