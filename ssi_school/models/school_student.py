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
        required=False,
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
        comodel_name="school_grade",
        related=False,
        compute="_compute_next_grade_id",
        store=True,
        compute_sudo=True,
    )
    enrollment_ids = fields.One2many(
        string="Enrollments",
        comodel_name="school_enrollment",
        inverse_name="student_id",
        readonly=True,
    )
    report_card_ids = fields.One2many(
        string="Report Cards",
        comodel_name="school_report_card",
        inverse_name="student_id",
        readonly=True,
    )
    latest_report_card_id = fields.Many2one(
        string="Lastest Report Card",
        comodel_name="school_report_card",
        compute="_compute_latest_report_card_id",
        store=True,
        compute_sudo=True,
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

    @api.depends(
        "report_card_ids",
        "report_card_ids.state",
        "report_card_ids.final_pass",
        "report_card_ids.last_term",
    )
    def _compute_latest_report_card_id(self):
        for record in self:
            result = False
            criteria = [
                ("student_id", "=", record.id),
                ("state", "=", "done"),
                ("final_pass", "=", True),
                ("last_term", "=", True),
            ]
            report_cards = self.env["school_report_card"].search(criteria)
            if len(report_cards) > 0:
                result = report_cards[0]
            record.latest_report_card_id = result

    @api.depends(
        "initial_grade_id",
        "enrollment_ids",
        "enrollment_ids.state",
        "latest_report_card_id",
    )
    def _compute_next_grade_id(self):
        for record in self:
            if not record.initial_grade_id and not record.enrollment_ids:
                result = self.env["school_grade"].search([])[0]
            elif record.initial_grade_id and not record.enrollment_ids:
                result = record.initial_grade_id.next_grade_id
            elif record.enrollment_ids and not record.latest_report_card_id:
                result = record.enrollment_ids[-1].grade_id
            elif record.enrollment_ids and record.latest_report_card_id:
                result = record.latest_report_card_id.grade_id.next_grade_id
            record.next_grade_id = result
