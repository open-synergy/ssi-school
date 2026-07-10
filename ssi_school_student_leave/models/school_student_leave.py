# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolStudentLeave(models.Model):
    """
    Represents a Student Leave of Absence transaction. Documents a
    student's temporary leave, valid for exactly one academic term,
    through a simplified approval workflow: Draft -> Confirm ->
    Approve -> Done (+ Cancel from draft/confirm/reject). On Done,
    the linked student (school_student) is transitioned to the
    on_leave state via action_set_to_on_leave(). The leave document
    itself is not reverted through the workflow: once the leave
    period is over, the Return button re-enrolls the student
    (action_set_to_enroll()) directly, with no separate approval
    step required.
    """

    _name = "school_student_leave"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
    ]
    _description = "Student Leave"

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
        help="The date the leave of absence document was created.",
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
        help="The student who is applying for a leave of absence.",
    )
    active_enrollment_id = fields.Many2one(
        string="Active Enrollment",
        comodel_name="school_enrollment",
        related="student_id.active_enrollment_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help=(
            "The student's currently active (open) enrollment, shown "
            "for reference when granting the leave."
        ),
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
        help=(
            "The single academic term during which the student is on "
            "leave. The leave is only valid for this term."
        ),
    )
    expected_return_date = fields.Date(
        string="Expected Return Date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The date the student is expected to return from leave "
            "and resume enrollment."
        ),
    )
    reason = fields.Text(
        string="Reason",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Explanation for why this leave of absence is requested.",
    )

    @api.constrains("state", "student_id")
    def _check_student_state_allowed(self):
        for record in self.sudo():
            if not record._check_student_state_allowed_condition():
                error_message = (
                    _(
                        """
Context: Change student leave state into %s
Database ID: %s
Problem: Student '%s' is not in enrol state
Solution: The student must be enrolled before this leave can be
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
    def _check_single_active_leave(self):
        for record in self.sudo():
            if not record._check_single_active_leave_condition():
                error_message = (
                    _(
                        """
Context: Change student leave state into %s
Database ID: %s
Problem: Another leave for student '%s' is already draft or waiting
for approval
Solution: Complete, reject, or cancel the other leave before
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

    def _check_single_active_leave_condition(self):
        self.ensure_one()
        if self.state not in ("draft", "confirm") or not self.student_id:
            return True
        duplicate = self.search(
            self._get_single_active_leave_criteria(),
        )
        return not duplicate

    def _get_single_active_leave_criteria(self):
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
Context: Complete student leave
Database ID: %s
Problem: Student '%s' is no longer in enrol state
Solution: Cancel this leave; the student must stay enrolled until
the leave is completed
"""
                )
                % (
                    self.id,
                    self.student_id.name,
                )
            )
            raise UserError(error_message)

    @ssi_decorator.post_done_action()
    def _20_apply_leave(self):
        self.ensure_one()
        self.student_id.sudo().action_set_to_on_leave()

    def action_return(self):
        for record in self.sudo():
            record._return()  # pylint: disable=protected-access

    def _return(self):
        self.ensure_one()
        if self.student_id.state != "on_leave":
            error_message = (
                _(
                    """
Context: Return student from leave
Database ID: %s
Problem: Student '%s' is not currently on leave
Solution: This action is only valid when the student is in on_leave
state
"""
                )
                % (
                    self.id,
                    self.student_id.name,
                )
            )
            raise UserError(error_message)
        self.student_id.sudo().action_set_to_enroll()

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
