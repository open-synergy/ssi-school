# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolStudentGraduation(models.Model):
    """
    Represents a Student Graduation transaction: the formal, auditable
    document that records a student's graduation from school. The
    document is a standalone document with a simplified approval
    workflow: Draft -> Confirm -> Approve -> Done (+ Cancel from
    draft/confirm/reject). Done is terminal: once applied, the
    graduation can no longer be cancelled or reverted. On Done, the
    student is moved to the "graduate" state (school_student.state,
    via the existing action_set_to_graduate method) and, if the
    student has an active enrollment, that enrollment's
    academic_year_result is set to "graduate".
    """

    _name = "school_student_graduation"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
    ]
    _description = "Student Graduation"

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
        help="The date this graduation document was created.",
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
        help="The student being graduated by this document.",
    )
    active_enrollment_id = fields.Many2one(
        string="Active Enrollment",
        comodel_name="school_enrollment",
        related="student_id.active_enrollment_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help=(
            "The student's currently active (open) enrollment, "
            "automatically taken from the student. Its academic year "
            "result is set to Graduate when this document reaches Done."
        ),
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        related="active_enrollment_id.academic_year_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The academic year of the student's active enrollment.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        related="active_enrollment_id.academic_term_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The academic term of the student's active enrollment.",
    )
    graduation_date = fields.Date(
        string="Graduation Date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The official date the student graduated.",
    )
    note = fields.Text(
        string="Note",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Additional notes or remarks about this graduation.",
    )

    @api.constrains("state", "student_id")
    def _check_student_state_allowed(self):
        for record in self.sudo():
            if not record._check_student_state_allowed_condition():
                error_message = (
                    _(
                        """
Context: Change student graduation state into %s
Database ID: %s
Problem: Student '%s' is not in enrolled state
Solution: The student must be enrolled before this graduation can be
confirmed or completed
"""
                    )
                    % (
                        record.state,
                        record.id,
                        record.student_id.name,
                    )
                )
                raise ValidationError(error_message)

    def _check_student_state_allowed_condition(self):
        self.ensure_one()
        if self.state not in ("confirm", "done"):
            return True
        return self.student_id.state == "enrol"

    @api.constrains("state", "student_id")
    def _check_single_active_graduation(self):
        for record in self.sudo():
            if not record._check_single_active_graduation_condition():
                error_message = (
                    _(
                        """
Context: Change student graduation state into %s
Database ID: %s
Problem: Another graduation for student '%s' is already draft or
waiting for approval
Solution: Complete, reject, or cancel the other graduation before
confirming this one
"""
                    )
                    % (
                        record.state,
                        record.id,
                        record.student_id.name,
                    )
                )
                raise ValidationError(error_message)

    def _check_single_active_graduation_condition(self):
        self.ensure_one()
        if self.state not in ("draft", "confirm") or not self.student_id:
            return True
        duplicate = self.search(
            self._get_single_active_graduation_criteria(),
        )
        return not duplicate

    def _get_single_active_graduation_criteria(self):
        self.ensure_one()
        return [
            ("id", "!=", self.id),
            ("student_id", "=", self.student_id.id),
            ("state", "in", ["draft", "confirm"]),
        ]

    @ssi_decorator.pre_done_check()
    def _10_check_ready(self):
        self.ensure_one()
        self._check_done_student_enrol()

    def _check_done_student_enrol(self):
        self.ensure_one()
        if self.student_id.state != "enrol":
            error_message = (
                _(
                    """
Context: Complete student graduation
Database ID: %s
Problem: Student '%s' is no longer enrolled
Solution: Cancel this graduation; the student must stay enrolled until
the graduation is completed
"""
                )
                % (
                    self.id,
                    self.student_id.name,
                )
            )
            raise ValidationError(error_message)

    @ssi_decorator.post_done_action()
    def _20_apply_graduation(self):
        self.ensure_one()
        self.student_id.sudo().action_set_to_graduate()

    @ssi_decorator.post_done_action()
    def _30_set_enrollment_result(self):
        self.ensure_one()
        if self.active_enrollment_id:
            self.active_enrollment_id.sudo().write(
                self._prepare_enrollment_result_vals()
            )

    def _prepare_enrollment_result_vals(self):
        self.ensure_one()
        return {
            "academic_year_result": "graduate",
        }

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "done_ok",
            "cancel_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
