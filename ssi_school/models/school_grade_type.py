# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class SchoolGradeType(models.Model):
    """
    Represents an education level type or school category.
    Used to group grades by education level, such as Elementary (SD),
    Junior High (SMP), or Senior High (SMA).
    Each school and grade belongs to one grade type.
    """

    _name = "school_grade_type"
    _inherit = ["mixin.master_data"]
    _description = "School Grade Type"
    _order = "sequence asc, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help="Display order of the grade type. Lower values appear first in the list.",
    )
