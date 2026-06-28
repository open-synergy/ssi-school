# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolAcademicTerm(models.Model):
    _name = "school_academic_term"
    _inherit = [
        "school_academic_term",
    ]

    is_open_admission = fields.Boolean(
        string="Open for Admission",
        default=False,
        help=(
            "Indicates whether this academic term is open for school admission. "
            "When enabled, this term will appear in the admission wizard."
        ),
    )
