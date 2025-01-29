# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import date as datetime_date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolClass(models.Model):
    _name = "school_class"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "School Class"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False

    _statusbar_visible_label = "draft,open,confirm,done"
    _policy_field_order = [
        "open_ok",
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_open",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    date = fields.Date(
        string="Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    curiculum_id = fields.Many2one(
        string="Curiculum",
        comodel_name="school_curiculum",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    subject_id = fields.Many2one(
        string="Subject",
        comodel_name="school_subject",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    scoring_system_id = fields.Many2one(
        string="Scoring System",
        comodel_name="school_scoring_system",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    num_of_student = fields.Integer(
        string="Num of Student",
        compute="_compute_num_of_student",
        store=True,
        compute_sudo=True,
    )
    seat_avalilable = fields.Integer(
        string="Seat Available",
        compute="_compute_num_of_student",
        store=True,
        compute_sudo=True,
    )
    class_capacity = fields.Integer(
        string="Capacity",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    class_assignment_ids = fields.One2many(
        string="Class Assignments",
        comodel_name="school_student_class_assignment",
        inverse_name="class_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "class_capacity",
        "class_assignment_ids",
    )
    def _compute_num_of_student(self):
        for record in self:
            num_of_student = len(record.class_assignment_ids)
            available = record.class_capacity - num_of_student
            record.num_of_student = num_of_student
            record.seat_avalilable = available

    @api.onchange(
        "academic_year_id",
    )
    def onchange_academic_term_id(self):
        self.academic_term_id = False

    @api.onchange(
        "grade_type_id",
    )
    def onchange_grade_id(self):
        self.grade_id = False

    @api.onchange(
        "grade_type_id",
    )
    def onchange_curiculum_id(self):
        self.curiculum_id = False
        if self.grade_type_id:
            criteria = [
                ("grade_type_id", "=", self.grade_type_id.id),
                ("state", "=", "open"),
            ]
            curiculums = self.env["school_curiculum"].search(criteria)
            if len(curiculums) > 0:
                self.curiculum_id = curiculums[0]

    def action_create_score_sheet(self):
        for record in self.sudo():
            record._create_score_sheet()

    def _create_score_sheet(self):
        self.ensure_one()
        for score_type in self.scoring_system_id.detail_ids:
            data = self._prepare_score_sheet()
            data.update(
                {
                    "score_type_id": score_type.score_type_id.id,
                }
            )
            score_sheet = self.env["school_student_score_sheet"].create(data)
            score_sheet.action_load_student_score()

    def _prepare_score_sheet(self):
        self.ensure_one()
        return {
            "date": datetime_date.today(),
            "academic_year_id": self.academic_year_id.id,
            "academic_term_id": self.academic_term_id.id,
            "grade_type_id": self.grade_type_id.id,
            "grade_id": self.grade_id.id,
            "class_id": self.id,
        }

    @api.model
    def _get_policy_field(self):
        res = super(SchoolClass, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
