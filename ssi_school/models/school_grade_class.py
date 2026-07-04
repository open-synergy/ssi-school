# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class SchoolGradeClass(models.Model):  # pylint: disable=too-few-public-methods
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
    capacity = fields.Integer(
        string="Capacity",
        default=0,
        help=(
            "Maximum number of students this class can hold. "
            "Leave at 0 for unlimited capacity (no enrollment cap is enforced)."
        ),
    )
    student_count = fields.Integer(
        string="Student Count",
        compute="_compute_student_count",
        help=(
            "Number of students currently actively enrolled (enrollment state "
            "Open) in this class."
        ),
    )
    available_seat = fields.Integer(
        string="Available Seat",
        compute="_compute_student_count",
        help=(
            "Remaining seats in this class (Capacity minus Student Count). "
            "Not meaningful when Capacity is 0 (unlimited)."
        ),
    )

    @api.onchange(
        "school_id",
    )
    def onchange_grade_id(self):
        self.grade_id = False

    # Deliberately non-store: student_count/available_seat aggregate
    # school_enrollment records on another model, so there is no field chain
    # to declare as a dependency. They recompute on every fresh read (e.g. a
    # freshly opened form); actual capacity enforcement lives in
    # school_enrollment._check_grade_class_capacity, which always runs a live
    # search_count and is unaffected by this field's caching.
    @api.depends("capacity")
    def _compute_student_count(self):
        enrollment_model = self.env["school_enrollment"]
        for record in self:
            count = enrollment_model.search_count(
                [("grade_class_id", "=", record.id), ("state", "=", "open")]
            )
            record.student_count = count
            record.available_seat = record.capacity - count
