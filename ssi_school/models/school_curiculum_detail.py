# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SchoolCuriculumDetail(models.Model):
    _name = "school_curiculum.detail"
    _description = "School Curiculum - Detail"
    _order = "curiculum_id, grade_id, subject_id"

    curiculum_id = fields.Many2one(
        string="Curiculum",
        comodel_name="school_curiculum",
        required=True,
        ondelete="cascade",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=True,
        ondelete="restrict",
    )
    subject_id = fields.Many2one(
        string="Subject",
        comodel_name="school_subject",
        required=True,
        ondelete="restrict",
    )
