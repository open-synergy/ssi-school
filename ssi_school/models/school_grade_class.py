# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class SchoolGradeClass(models.Model):
    """
    Represents a homeroom class (class group) within a school.
    A grade class is a concrete class unit formed from the combination of a school
    and a grade level, e.g. 'Grade 1A' or 'Grade 2B' at a specific school.
    The grade_type_id field is automatically populated from the selected school.
    """

    _name = "school_grade_class"
    _inherit = ["mixin.master_data"]
    _description = "School Grade Class"

    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        ondelete="restrict",
        help="The school where this homeroom class is located.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        store=True,
        help="The grade type from the selected school, populated automatically.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=True,
        ondelete="restrict",
        help=(
            "The class level for this homeroom, e.g. Grade 1 or Grade 2. "
            "Will be reset if the school is changed."
        ),
    )

    @api.onchange(
        "school_id",
    )
    def onchange_grade_id(self):
        self.grade_id = False
