# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SchoolStudentClassAssignment(models.Model):
    _name = "school_student_class_assignment"
    _description = "School Student Class Assigment"

    enrollment_id = fields.Many2one(
        string="# Enrollment",
        comodel_name="school_enrollment",
        required=True,
        ondelete="cascade",
    )
    report_card_id = fields.Many2one(
        string="# Report Card",
        related="enrollment_id.report_card_id",
        store=True,
    )
    student_id = fields.Many2one(
        string="Student",
        related="enrollment_id.student_id",
        store=True,
    )
    subject_id = fields.Many2one(
        string="Subject",
        comodel_name="school_subject",
        ondelete="restrict",
        required=True,
    )
    class_id = fields.Many2one(
        string="# Class",
        comodel_name="school_class",
        ondelete="set null",
    )
    score_ids = fields.One2many(
        string="Scores",
        comodel_name="school_student_score",
        inverse_name="class_assignment_id",
    )
    score = fields.Float(
        string="Score",
        compute="_compute_score",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "score_ids",
        "score_ids.final_score",
    )
    def _compute_score(self):
        for record in self:
            result = 0.0
            for score in record.score_ids:
                result += score.final_score
            record.score = result

    def action_load_assignment(self):
        for record in self.sudo():
            record._load_assignment()

    def _load_assignment(self):
        self.ensure_one()
        if self.class_id:
            return True

        criteria = [
            ("academic_term_id", "=", self.enrollment_id.academic_term_id.id),
            ("subject_id", "=", self.subject_id.id),
            ("state", "=", "open"),
            ("grade_id", "=", self.enrollment_id.grade_id.id),
        ]

        classes = self.env["school_class"].search(criteria)

        if len(classes) > 0:
            self.write(
                {
                    "class_id": classes[0].id,
                }
            )
