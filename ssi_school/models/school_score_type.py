# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models


class SchoolScoreType(models.Model):
    _name = "school_score_type"
    _inherit = ["mixin.master_data"]
    _description = "School Score Type"
