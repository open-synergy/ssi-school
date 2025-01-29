# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolStudentScoreSheet(models.Model):
    _name = "school_student_score_sheet"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
    ]
    _description = "School Student Score Sheet Sheet"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

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
    class_id = fields.Many2one(
        string="# Class",
        comodel_name="school_class",
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
        related="class_id.teacher_id",
        store=True,
    )
    score_type_id = fields.Many2one(
        string="Score Type",
        comodel_name="school_score_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    score_ids = fields.One2many(
        string="Scores",
        comodel_name="school_student_score",
        inverse_name="sheet_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    def action_load_student_score(self):
        for record in self.sudo():
            record._load_student_score()

    def _load_student_score(self):
        self.ensure_one()
        for assignment in self.class_id.class_assignment_ids:
            data = self._prepare_student_score()
            data.update(
                {
                    "class_assignment_id": assignment.id,
                }
            )
            self.env["school_student_score"].create(data)

    def _prepare_student_score(self):
        self.ensure_one()
        return {
            "sheet_id": self.id,
        }

    @api.model
    def _get_policy_field(self):
        res = super(SchoolStudentScoreSheet, self)._get_policy_field()
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
