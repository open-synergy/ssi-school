# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolAcademicYear(models.Model):
    """
    Extends School Academic Year with multiple operating unit support
    for operating unit-based data segregation.
    """

    _name = "school_academic_year"
    _inherit = [
        "school_academic_year",
        "mixin.multiple_operating_unit",
    ]
