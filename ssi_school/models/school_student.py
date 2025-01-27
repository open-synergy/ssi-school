# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class SchoolStudent(models.Model):
    _name = "school_student"
    _inherit = ["mixin.master_data"]
    _description = "Student"

    contact_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
    )
    initial_grade_id = fields.Many2one(
        string="Initial Grade",
        comodel_name="school_grade",
        required=True,
    )
    initial_grade_type_id = fields.Many2one(
        string="Initial Grade Type",
        related="current_grade_id.type_id",
        store=True,
    )
    current_grade_id = fields.Many2one(
        string="Current Grade",
        comodel_name="school_grade",
        compute="_compute_current_grade_id",
        store=True,
        compute_sudo=True,
    )
    current_grade_type_id = fields.Many2one(
        string="Current Grade Type",
        related="current_grade_id.type_id",
        store=True,
    )
    next_grade_id = fields.Many2one(
        string="Next Grade",
        related="current_grade_id.next_grade_id",
        store=True,
    )
    enrollment_ids = fields.One2many(
        string="Enrollments",
        comodel_name="school_enrollment",
        inverse_name="student_id",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Waiting for Enrollment"),
            ("enrol", "Enrolled"),
            ("graduate", "Graduated"),
        ],
        default="draft",
    )

    @api.depends("initial_grade_id", "enrollment_ids", "enrollment_ids.state")
    def _compute_current_grade_id(self):
        for record in self:
            result = record.initial_grade_id
            criteria = [
                ("state", "in", ["open", "done"]),
                ("student_id", "=", record.id),
            ]
            enrollments = self.env["school_enrollment"].search(criteria)
            if len(enrollments) > 0:
                result = enrollments[-1].grade_id
            record.current_grade_id = result
