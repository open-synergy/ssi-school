# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolGradeClass(models.Model):
    _name = "school_grade_class"
    _inherit = [
        "school_grade_class",
        "mixin.multiple_operating_unit",
    ]
