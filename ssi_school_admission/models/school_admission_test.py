# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolAdmissionTest(models.Model):
    _name = "school_admission_test"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "School Admission Test"

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
        "create_school_admission_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_done",
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
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
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
        related="school_id.grade_type_id",
        store=True,
        compute_sudo=True,
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
    admission_form_id = fields.Many2one(
        string="Admission Form",
        comodel_name="school_admission_form",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    passed = fields.Boolean(
        string="Passed",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    create_school_admission_ok = fields.Boolean(
        string="Can Create School Admission",
        compute="_compute_policy",
        compute_sudo=True,
    )

    @api.constrains("admission_form_id")
    def _check_admission_form_uniqueness(self):
        for record in self:
            if record.admission_form_id:
                existing = self.search(
                    [
                        ("admission_form_id", "=", record.admission_form_id.id),
                        ("id", "!=", record.id),
                    ]
                )
                if existing:
                    raise ValidationError(
                        _("Admission Form %s already has an Admission Test.")
                        % record.admission_form_id.name
                    )

    @api.onchange("academic_year_id")
    def _onchange_academic_term_id(self):
        self.academic_term_id = False

    @api.onchange("school_id")
    def _onchange_grade_id(self):
        self.grade_id = False

    @api.onchange("admission_form_id")
    def _onchange_student_id(self):
        if self.admission_form_id:
            self.student_id = self.admission_form_id.student_id
        else:
            self.student_id = False

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "done_ok",
            "cancel_ok",
            "open_ok",
            "restart_ok",
            "manual_number_ok",
            "restart_approval_ok",
            "create_school_admission_ok",
        ]
        res += policy_field
        return res
