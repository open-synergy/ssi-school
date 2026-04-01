# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolAcademicTerm(models.Model):
    """
    Extends School Academic Term with multiple operating unit support
    for operating unit-based data segregation.
    """

    _name = "school_academic_term"
    _inherit = [
        "school_academic_term",
        "mixin.multiple_operating_unit",
    ]
