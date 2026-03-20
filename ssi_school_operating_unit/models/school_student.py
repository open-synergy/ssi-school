# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolStudent(models.Model):
    _name = "school_student"
    _inherit = [
        "school_student",
        "mixin.multiple_operating_unit",
    ]
