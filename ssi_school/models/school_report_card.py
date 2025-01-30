# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolReportCard(models.Model):
    _name = "school_report_card"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.localdict",
    ]
    _description = "School Report Card"

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
    date = fields.Date(
        string="Date",
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
    last_term = fields.Boolean(
        string="Last Term of Academic Year?",
        related="academic_term_id.last_term",
        store=True,
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
    enrollment_id = fields.Many2one(
        string="# Enrollment",
        comodel_name="school_enrollment",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
    override_pass_result = fields.Boolean(
        string="Override Pass/ Result",
        default=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    auto_pass = fields.Boolean(
        string="Pass to Next Grade? (Automatic)",
        compute="_compute_auto_pass",
        store=True,
        compute_sudo=True,
    )
    override_reason = fields.Text(
        string="Override Reason",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    final_pass = fields.Boolean(
        string="Pass to Next Grade? (Final Decision)",
        compute="_compute_final_pass",
        store=True,
        compute_sudo=True,
    )
    class_assignment_ids = fields.One2many(
        string="Class Assignments",
        comodel_name="school_student_class_assignment",
        inverse_name="report_card_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "class_assignment_ids",
        "class_assignment_ids.score",
    )
    def _compute_auto_pass(self):
        for record in self:
            result = record._get_automatic_result()
            record.auto_pass = result

    @api.depends(
        "override_pass_result",
        "auto_pass",
    )
    def _compute_final_pass(self):
        for record in self:
            result = record.auto_pass
            if record.override_pass_result:
                result = not record.auto_pass
            record.final_pass = result

    def _get_automatic_result(self):
        self.ensure_one()
        localdict = self._get_default_localdict()
        try:
            safe_eval(
                self.enrollment_id.homeroom_id.pass_criteria_id.python_code,
                localdict,
                mode="exec",
                nocopy=True,
            )
            result = localdict["result"]
        except Exception:
            result = False
        return result

    @api.model
    def _get_policy_field(self):
        res = super(SchoolReportCard, self)._get_policy_field()
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
