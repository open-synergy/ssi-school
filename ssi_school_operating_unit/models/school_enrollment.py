# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolEnrollment(models.Model):
    _name = "school_enrollment"
    _inherit = [
        "school_enrollment",
        "mixin.single_operating_unit",
    ]
