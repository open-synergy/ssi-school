# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolStudent(models.Model):
    _name = "school_student"
    _inherit = ["school_student", "mixin.qr_code"]

    _qr_code_create_page = True
