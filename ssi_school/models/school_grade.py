# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class SchoolGrade(models.Model):
    _name = "school_grade"
    _inherit = ["mixin.master_data"]
    _description = "School Grade"
    _order = "type_id asc, sequence asc, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="school_grade_type",
        required=True,
        ondelete="restrict",
    )
