# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class School(models.Model):
    _name = "school"
    _inherit = [
        "school",
        "mixin.multiple_operating_unit",
    ]
