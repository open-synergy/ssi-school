# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolStudentGraduationBatchLine(models.Model):
    """
    Represents one student selected for processing within a Student
    Graduation Batch. Each line drives the creation and workflow of a
    single school_student_graduation document; the resulting document
    is kept on graduation_id as an audit trail once processed.
    """

    _name = "school_student_graduation_batch_line"
    _description = "Student Graduation Batch Line"
    _order = "batch_id, id"

    batch_id = fields.Many2one(
        string="# Batch",
        comodel_name="school_student_graduation_batch",
        required=True,
        ondelete="cascade",
        help="The Student Graduation Batch this line belongs to.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        required=True,
        help="The student selected to be graduated by this batch.",
    )
    graduation_id = fields.Many2one(
        string="Graduation",
        comodel_name="school_student_graduation",
        readonly=True,
        help=(
            "The Student Graduation document generated for this line "
            "once the batch is Done. Empty until the batch is "
            "processed."
        ),
    )
