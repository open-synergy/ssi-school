# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolEnrollment(models.Model):
    _name = "school_enrollment"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "School Enrollment"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
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
    allowed_student_ids = fields.Many2many(
        string="Allowed Students",
        comodel_name="school_student",
        compute="_compute_allowed_student_ids",
        store=False,
        compute_sudo=True,
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    homeroom_id = fields.Many2one(
        string="# Homeroom",
        comodel_name="school_homeroom",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    report_card_id = fields.Many2one(
        string="# Report Card",
        comodel_name="school_report_card",
        required=False,
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
        inverse_name="enrollment_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "academic_term_id",
        "grade_id",
    )
    def _compute_allowed_student_ids(self):
        for record in self:
            result = False
            if record.academic_term_id and record.grade_id:
                criteria = [
                    ("state", "=", "draft"),
                ]
                if record.academic_term_id.first_term:
                    criteria += [("next_grade_id", "=", record.grade_id.id)]
                else:
                    criteria += [("current_grade_id", "=", record.grade_id.id)]
                result = self.env["school_student"].search(criteria).ids
            record.allowed_student_ids = result

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

    @api.onchange(
        "academic_term_id",
        "grade_id",
    )
    def onchange_homeroom_id(self):
        self.homeroom_id = False

    @api.onchange(
        "academic_term_id",
        "grade_id",
    )
    def onchange_student_id(self):
        self.student_id = False

    def action_load_assignment(self):
        for record in self.sudo():
            record._load_assignment()

    def _load_assignment(self):
        self.ensure_one()
        self.class_assignment_ids.unlink()
        criteria = [
            ("curiculum_id", "=", self.curiculum_id.id),
        ]
        for detail in self.env["school_curiculum.detail"].search(criteria):
            data = {
                "enrollment_id": self.id,
                "subject_id": detail.subject_id.id,
            }
            detail = self.env["school_student_class_assignment"].create(data)
            detail._load_assignment()

    @ssi_decorator.post_open_action()
    def _create_report_card(self):
        self.ensure_one()
        if self.report_card_id:
            return True

        data = self._prepare_report_card()
        report_card = self.env["school_report_card"].create(data)
        self.write(
            {
                "report_card_id": report_card.id,
            }
        )

    def _prepare_report_card(self):
        self.ensure_one()
        return {
            "academic_year_id": self.academic_year_id.id,
            "academic_term_id": self.academic_term_id.id,
            "date": self.date,
            "grade_type_id": self.grade_type_id.id,
            "grade_id": self.grade_id.id,
            "curiculum_id": self.curiculum_id.id,
            "enrollment_id": self.id,
            "student_id": self.student_id.id,
        }

    @api.model
    def _get_policy_field(self):
        res = super(SchoolEnrollment, self)._get_policy_field()
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
