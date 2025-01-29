# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SchoolStudentScore(models.Model):
    _name = "school_student_score"
    _description = "School Student Score"

    sheet_id = fields.Many2one(
        string="# Score Sheet",
        comodel_name="school_student_score_sheet",
        required=True,
        ondelete="cascade",
    )
    class_assignment_id = fields.Many2one(
        string="Class Assignment",
        comodel_name="school_student_class_assignment",
        ondelete="restrict",
        required=True,
    )
    student_id = fields.Many2one(
        string="Student",
        related="class_assignment_id.student_id",
        store=True,
    )
    score = fields.Float(
        string="Score",
        required=True,
        default=0.0,
    )
    percentage = fields.Float(
        string="Percentage",
        compute="_compute_percentage",
        store=True,
        compute_sudo=True,
    )
    final_score = fields.Float(
        string="Final Score",
        compute="_compute_final_score",
        store=True,
        compute_sudo=True,
    )

    @api.depends("sheet_id.class_id.scoring_system_id")
    def _compute_percentage(self):
        for record in self:
            result = 0.0
            scoring_system = record.sheet_id.class_id.scoring_system_id
            score_type = record.sheet_id.score_type_id
            criteria = [
                ("scoring_system_id", "=", scoring_system.id),
                ("score_type_id", "=", score_type.id),
            ]
            details = self.env["school_scoring_system.detail"].search(criteria)
            if len(details) > 0:
                result = details[0].percentage
            record.percentage = result

    @api.depends(
        "percentage",
        "score",
    )
    def _compute_final_score(self):
        for record in self:
            record.final_score = record.score * (record.percentage / 100.00)
