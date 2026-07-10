# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolStudentGraduationBatch(models.Model):
    """
    Represents a Student Graduation Batch: a cohort-level transaction
    that graduates many students at once while preserving a full
    per-student audit trail. Rather than writing student/enrollment
    state directly, the batch generates one school_student_graduation
    document per selected student line and drives each through its
    own confirm/done transition, so every guard and side effect
    defined on the individual document (student state check,
    single-active-graduation check, enrollment result update, ...)
    still applies. Follows the same simplified approval workflow as
    Student Graduation: Draft -> Confirm -> Approve -> Done (+ Cancel
    from draft/confirm/reject). Done is terminal.
    """

    _name = "school_student_graduation_batch"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
    ]
    _description = "Student Graduation Batch"

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
        help="The date this graduation batch document was created.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "Optional filter: when set, only students whose active "
            "enrollment belongs to this academic year are proposed "
            "when populating lines."
        ),
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "Optional filter: when set, only students whose active "
            "enrollment belongs to this academic term are proposed "
            "when populating lines."
        ),
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "Optional filter: when set, only students whose active "
            "enrollment belongs to this grade are proposed when "
            "populating lines."
        ),
    )
    line_ids = fields.One2many(
        string="Lines",
        comodel_name="school_student_graduation_batch_line",
        inverse_name="batch_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "Students selected to be graduated by this batch. Can be "
            "populated automatically from the filters above, or "
            "managed manually."
        ),
    )

    def action_populate_lines(self):
        for record in self.sudo():
            record._populate_lines()

    def _populate_lines(self):
        self.ensure_one()
        self.line_ids = [(5, 0, 0)]
        students = self.env["school_student"].search(
            self._get_eligible_student_criteria()
        )
        line_vals = []
        for student in students:
            line_vals.append((0, 0, self._prepare_batch_line_data(student)))
        self.line_ids = line_vals

    def _get_eligible_student_criteria(self):
        self.ensure_one()
        criteria = [
            ("state", "=", "enrol"),
            ("next_grade_id", "=", False),
        ]
        if self.academic_year_id:
            criteria.append(
                (
                    "active_enrollment_id.academic_year_id",
                    "=",
                    self.academic_year_id.id,
                )
            )
        if self.academic_term_id:
            criteria.append(
                (
                    "active_enrollment_id.academic_term_id",
                    "=",
                    self.academic_term_id.id,
                )
            )
        if self.grade_id:
            criteria.append(
                (
                    "active_enrollment_id.grade_id",
                    "=",
                    self.grade_id.id,
                )
            )
        return criteria

    def _prepare_batch_line_data(self, student):
        self.ensure_one()
        return {
            "student_id": student.id,
        }

    @ssi_decorator.pre_done_check()
    def _10_check_ready(self):
        self.ensure_one()
        self._check_done_has_lines()
        self._check_done_lines_student_enrol()

    def _check_done_has_lines(self):
        self.ensure_one()
        if not self.line_ids:
            error_message = (
                _(
                    """
Context: Complete student graduation batch
Database ID: %s
Problem: No student line has been added to this batch
Solution: Populate or add at least one student line before completing
this batch
"""
                )
                % (self.id,)
            )
            raise ValidationError(error_message)

    def _check_done_lines_student_enrol(self):
        self.ensure_one()
        invalid_students = self.line_ids.filtered(
            lambda line: line.student_id.state != "enrol"
        ).mapped("student_id.name")
        if invalid_students:
            error_message = (
                _(
                    """
Context: Complete student graduation batch
Database ID: %s
Problem: Status check ineligible student(s) failed: %s
Solution: Remove the ineligible student line(s), or ensure every
selected student is still in the enrolled state, before completing
this batch
"""
                )
                % (
                    self.id,
                    ", ".join(invalid_students),
                )
            )
            raise ValidationError(error_message)

    @ssi_decorator.post_done_action()
    def _20_process_lines(self):
        self.ensure_one()
        for line in self.line_ids:
            self._process_graduation_line(line)

    def _process_graduation_line(self, line):
        self.ensure_one()
        graduation = self.env["school_student_graduation"].create(
            self._prepare_graduation_data(line)
        )
        # The batch's own confirm/approve cycle already authorized this
        # mass action, so each generated document is driven straight to
        # Done under bypass_policy_check: going through the standard
        # action_approve_approval() would additionally require the user
        # executing the batch to be a registered approver on the
        # per-student Student Graduation approval template too, which
        # is not guaranteed to be the same group as the batch
        # validators. Every per-student business guard (constrains,
        # pre_done_check) still runs normally and can still roll back
        # the whole batch transaction.
        graduation.with_context(bypass_policy_check=True).action_confirm()
        graduation.with_context(bypass_policy_check=True).action_done()
        line.write({"graduation_id": graduation.id})

    def _prepare_graduation_data(self, line):
        self.ensure_one()
        return {
            "date": self.date,
            "student_id": line.student_id.id,
            "graduation_date": self.date,
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
