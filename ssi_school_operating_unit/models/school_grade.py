# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolGrade(models.Model):
    """
    Extends School Grade with multiple operating unit support
    for operating unit-based data segregation.
    """

    _name = "school_grade"
    _inherit = [
        "school_grade",
        "mixin.multiple_operating_unit",
    ]
