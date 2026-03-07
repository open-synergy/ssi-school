# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class School(models.Model):
    _name = "school"
    _inherit = ["mixin.master_data"]
    _description = "School"

    grade_type_id = fields.Many2one(
        "school_grade_type",
        string="Grade Type",
        required=True,
    )
