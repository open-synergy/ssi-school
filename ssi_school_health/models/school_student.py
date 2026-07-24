# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolStudent(models.Model):
    """
    Exposes the health data of the linked contact (res.partner) on the
    student record, so that school staff can read and maintain it without
    leaving the student form. No health data is stored on the student
    itself: every field below is related to the contact, which remains the
    single source of truth.
    """

    _name = "school_student"
    _inherit = ["school_student"]

    height_ids = fields.One2many(
        string="Heights",
        related="contact_id.height_ids",
        readonly=False,
        help="Height measurement history of the student, "
        "managed through the linked contact.",
    )
    weight_ids = fields.One2many(
        string="Weights",
        related="contact_id.weight_ids",
        readonly=False,
        help="Weight measurement history of the student, "
        "managed through the linked contact.",
    )
    head_circumference_ids = fields.One2many(
        string="Head Circumferences",
        related="contact_id.head_circumference_ids",
        readonly=False,
        help="Head circumference measurement history of the student, "
        "managed through the linked contact.",
    )
    allergy_ids = fields.One2many(
        string="Allergies",
        related="contact_id.allergy_ids",
        readonly=False,
        help="Allergies recorded for the student, "
        "managed through the linked contact.",
    )
    disease_history_ids = fields.One2many(
        string="Disease History",
        related="contact_id.disease_history_ids",
        readonly=False,
        help="Disease history recorded for the student, "
        "managed through the linked contact.",
    )
    height = fields.Float(
        string="Height (cm)",
        related="contact_id.height",
        store=True,
        readonly=True,
        help="Latest recorded height (cm) of the student, taken from the "
        "contact. Read-only: change it by adding a height measurement.",
    )
    weight = fields.Float(
        string="Weight (kg)",
        related="contact_id.weight",
        store=True,
        readonly=True,
        help="Latest recorded weight (kg) of the student, taken from the "
        "contact. Read-only: change it by adding a weight measurement.",
    )
    head_circumference = fields.Float(
        string="Head Circumference (cm)",
        related="contact_id.head_circumference",
        store=True,
        readonly=True,
        help="Latest recorded head circumference (cm) of the student, taken "
        "from the contact. Read-only: change it by adding a head "
        "circumference measurement.",
    )
