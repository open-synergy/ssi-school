# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolGradeType(models.Model):
    _name = "school_grade_type"
    _inherit = [
        "school_grade_type",
        "mixin.multiple_operating_unit",
    ]
