# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolTeacher(models.Model):
    """
    Extends School Teacher with multiple operating unit support
    for operating unit-based data segregation.
    """

    _name = "school_teacher"
    _inherit = [
        "school_teacher",
        "mixin.multiple_operating_unit",
    ]
