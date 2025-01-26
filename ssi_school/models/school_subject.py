# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import models


class SchoolSubject(models.Model):
    _name = "school_subject"
    _inherit = ["mixin.master_data"]
    _description = "School Subject"
