# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class School(models.Model):
    """
    Represents a school entity.
    A school is associated with one grade type that defines the class level
    structure used within it. Inherits from mixin.master_data.
    """

    _name = "school"
    _inherit = ["mixin.master_data"]
    _description = "School"

    grade_type_id = fields.Many2one(
        "school_grade_type",
        string="Grade Type",
        required=True,
        help=(
            "The education level type used by this school, "
            "e.g. Elementary, Junior High, or Senior High School."
        ),
    )
