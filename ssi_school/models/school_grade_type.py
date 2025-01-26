# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class SchoolGradeType(models.Model):
    _name = "school_grade_type"
    _inherit = ["mixin.master_data"]
    _description = "School Grade Type"
    _order = "sequence asc, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
