# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolAdmissionPaymentTerm(models.Model):
    """
    Lets a promotion code be redeemed directly against one admission
    payment term.

    Carries ``mixin.promotion_object`` so each payment term line
    tracks its own Promotion Code Usages and exposes its own eligible
    receivable journal item to ``action_populate_allocation``. Billing
    granularity for promotions is per payment term, not per admission:
    ``_promotion_move_line_field_name`` follows ``customer_invoice_id``
    -- the invoice this term itself issued via
    ``action_create_invoice`` -- down to that invoice's own
    ``receivable_move_line_id``, and
    ``_promotion_partner_id_field_name`` reuses this term's own
    ``partner_id``, which is related straight to
    ``admission_id.student_id`` -- a ``res.partner`` on its own, with
    no ``contact_id`` hop, unlike the enrollment side. Neither
    attribute needs an override: both targets are plain field paths
    already present on this model and on ``customer_invoice``.

    Nothing here writes back to the payment term: ``promotion_usage_ids``
    is a non-stored compute and applying a promotion only creates a new
    ``promotion_code_usage``. A term already ``locked`` because its
    admission was opened therefore stays promotable, and that is the
    intended behaviour.
    """

    _name = "school_admission_payment_term"
    _inherit = [
        "school_admission_payment_term",
        "mixin.promotion_object",
    ]

    _promotion_move_line_field_name = "customer_invoice_id.receivable_move_line_id"
    _promotion_partner_id_field_name = "partner_id"
