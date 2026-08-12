# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolStudentMutation(models.Model):
    """
    Represents a Student Class Mutation transaction: moving a student's
    open enrollment from one grade class to another within the same
    grade and school (e.g. 1A to 1B), without touching the enrollment's
    grade, academic year/term, or billing. The mutation is a standalone,
    auditable document with a simplified approval workflow:
    Draft -> Confirm -> Approve -> Done (+ Cancel from draft/confirm/
    reject). Done is terminal: once applied, the mutation can no longer
    be cancelled or reverted. To undo a completed mutation, a new
    mutation document in the opposite direction (destination -> source)
    must be created. On Done, the linked enrollment's grade_class_id and
    homeroom_id are updated, which cascades into
    school_student.grade_class_id (related) and
    school_homeroom.enrolled_count (computed from enrollment_ids).
    """

    _name = "school_student_mutation"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
    ]
    _description = "Student Class Mutation"

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
        help="The date the class mutation document was created.",
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
        help="The student whose grade class is being mutated.",
    )
    allowed_enrollment_ids = fields.Many2many(
        string="Allowed Enrollments",
        comodel_name="school_enrollment",
        compute="_compute_allowed_enrollment_ids",
        store=False,
        compute_sudo=True,
        help=(
            "The student's enrollment(s) currently in open state, "
            "eligible to be selected as the enrollment to mutate."
        ),
    )
    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The student's open enrollment whose grade class and "
            "homeroom will be changed by this mutation."
        ),
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        related="enrollment_id.academic_year_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The academic year of the enrollment being mutated.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        related="enrollment_id.academic_term_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The academic term of the enrollment being mutated.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        related="enrollment_id.school_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The school of the enrollment being mutated.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        related="enrollment_id.grade_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help=(
            "The grade of the enrollment being mutated. Mutation only "
            "moves the student between grade classes within this same "
            "grade."
        ),
    )
    source_grade_class_id = fields.Many2one(
        string="Source Grade Class",
        comodel_name="school_grade_class",
        readonly=True,
        help=(
            "Snapshot of the enrollment's grade class before mutation, "
            "filled automatically when the Enrollment is selected. Kept "
            "unchanged after Done as an audit trail of the origin class."
        ),
    )
    source_homeroom_id = fields.Many2one(
        string="Source Homeroom",
        comodel_name="school_homeroom",
        readonly=True,
        help=(
            "Snapshot of the enrollment's homeroom before mutation, "
            "filled automatically when the Enrollment is selected. Kept "
            "unchanged after Done as an audit trail of the origin "
            "homeroom."
        ),
    )
    allowed_destination_grade_class_ids = fields.Many2many(
        string="Allowed Destination Grade Classes",
        comodel_name="school_grade_class",
        compute="_compute_allowed_destination_grade_class_ids",
        store=False,
        compute_sudo=True,
        help=(
            "Grade classes eligible as mutation destination: same grade "
            "and school as the enrollment, excluding the source class."
        ),
    )
    destination_grade_class_id = fields.Many2one(
        string="Destination Grade Class",
        comodel_name="school_grade_class",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The grade class the student will be moved into. Must "
            "belong to the same grade and school as the current "
            "enrollment."
        ),
    )
    destination_homeroom_id = fields.Many2one(
        string="Destination Homeroom",
        comodel_name="school_homeroom",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The open Homeroom batch for the destination class, if any. "
            "Automatically searched when the Destination Grade Class is "
            "selected, but may be left empty if no batch exists."
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
        help="Optional explanation for why this class mutation is made.",
    )

    @api.depends("student_id")
    def _compute_allowed_enrollment_ids(self):
        """List the enrollments this mutation may be applied to.

        Nothing is proposed until ``student_id`` is set; otherwise the
        ``school_enrollment`` records matching
        ``_get_allowed_enrollment_criteria`` — the enrollments of that
        student still in state ``open`` — are collected. The view uses
        the field to restrict the ``enrollment_id`` selection.
        """
        for record in self:
            result = False
            if record.student_id:
                criteria = record._get_allowed_enrollment_criteria()
                result = self.env["school_enrollment"].search(criteria).ids
            record.allowed_enrollment_ids = result

    def _get_allowed_enrollment_criteria(self):
        """Return the domain of enrollments eligible for mutation.

        Extension point of ``_compute_allowed_enrollment_ids``: override
        it to widen or narrow the selection. Matches the enrollments of
        ``student_id`` whose state is ``open``.

        :return: search domain for ``school_enrollment``.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        return [
            ("student_id", "=", self.student_id.id),
            ("state", "=", "open"),
        ]

    @api.depends("enrollment_id")
    def _compute_allowed_destination_grade_class_ids(self):
        """List the classes the student may be moved into.

        Nothing is proposed until ``enrollment_id`` is set; otherwise
        the ``school_grade_class`` records matching
        ``_get_allowed_destination_grade_class_criteria`` are collected.
        The view uses the field to restrict the
        ``destination_grade_class_id`` selection.
        """
        for record in self:
            result = False
            if record.enrollment_id:
                criteria = record._get_allowed_destination_grade_class_criteria()
                result = self.env["school_grade_class"].search(criteria).ids
            record.allowed_destination_grade_class_ids = result

    def _get_allowed_destination_grade_class_criteria(self):
        """Return the domain of eligible destination classes.

        Extension point of
        ``_compute_allowed_destination_grade_class_ids``: override it to
        change which classes may be picked. Matches the grade classes of
        the same grade and school as ``enrollment_id``, excluding the
        class the enrollment already sits in.

        :return: search domain for ``school_grade_class``.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        return [
            ("grade_id", "=", self.enrollment_id.grade_id.id),
            ("school_id", "=", self.enrollment_id.school_id.id),
            ("id", "!=", self.enrollment_id.grade_class_id.id),
        ]

    @api.onchange(
        "student_id",
    )
    def onchange_enrollment_id(self):
        self.enrollment_id = False
        if self.student_id:
            self.enrollment_id = self.student_id.active_enrollment_id

    @api.onchange(
        "enrollment_id",
    )
    def onchange_source_grade_class_id(self):
        self.source_grade_class_id = False
        if self.enrollment_id:
            self.source_grade_class_id = self.enrollment_id.grade_class_id

    @api.onchange(
        "enrollment_id",
    )
    def onchange_source_homeroom_id(self):
        self.source_homeroom_id = False
        if self.enrollment_id:
            self.source_homeroom_id = self.enrollment_id.homeroom_id

    @api.onchange(
        "enrollment_id",
    )
    def onchange_destination_grade_class_id(self):
        self.destination_grade_class_id = False

    @api.onchange(
        "enrollment_id",
        "destination_grade_class_id",
    )
    def onchange_destination_homeroom_id(self):
        """Propose the open Homeroom batch of the destination class.

        Clears ``destination_homeroom_id`` whenever ``enrollment_id`` or
        ``destination_grade_class_id`` changes, then fills it with the
        first ``school_homeroom`` matching
        ``_get_destination_homeroom_criteria``. The field legitimately
        stays empty when the destination class has no open batch.
        """
        self.destination_homeroom_id = False
        if self.destination_grade_class_id:
            criteria = self._get_destination_homeroom_criteria()
            self.destination_homeroom_id = self.env["school_homeroom"].search(
                criteria, limit=1
            )

    def _get_destination_homeroom_criteria(self):
        """Return the domain locating the destination Homeroom batch.

        Extension point of ``onchange_destination_homeroom_id``:
        override it to change how the batch is matched. Requires the
        same academic year, academic term and grade as
        ``enrollment_id``, the chosen ``destination_grade_class_id``,
        and state ``open``.

        :return: search domain for ``school_homeroom``.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        return [
            ("academic_year_id", "=", self.enrollment_id.academic_year_id.id),
            ("academic_term_id", "=", self.enrollment_id.academic_term_id.id),
            ("grade_id", "=", self.enrollment_id.grade_id.id),
            ("grade_class_id", "=", self.destination_grade_class_id.id),
            ("state", "=", "open"),
        ]

    @api.constrains("destination_grade_class_id", "enrollment_id")
    def _check_destination_distinct(self):
        """Enforce that the mutation really changes the class.

        Runs on every create or write touching
        ``destination_grade_class_id`` or ``enrollment_id`` and
        delegates the test to ``_check_destination_distinct_condition``,
        so an empty mutation can never be recorded.

        :raises ValidationError: the destination class is the class the
            enrollment already sits in.
        """
        for record in self.sudo():
            if not record._check_destination_distinct_condition():
                error_message = (
                    _(
                        """
Context: Set class mutation destination
Database ID: %s
Problem: Destination Grade Class '%s' is the same as the current class
Solution: Select a different Grade Class as the mutation destination
"""
                    )
                    % (
                        record.id,
                        record.destination_grade_class_id.name,
                    )
                )
                raise ValidationError(error_message)

    def _check_destination_distinct_condition(self):
        """Return whether the destination differs from the source.

        Extension point of the ``_check_destination_distinct``
        constraint: override it to change the rule. A record still
        missing the destination class or the enrollment is accepted,
        otherwise ``destination_grade_class_id`` must differ from
        ``enrollment_id.grade_class_id``.

        :return: ``True`` when the destination is another class.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if not self.destination_grade_class_id or not self.enrollment_id:
            return True
        return self.destination_grade_class_id != self.enrollment_id.grade_class_id

    @api.constrains("destination_grade_class_id", "enrollment_id")
    def _check_same_grade_school(self):
        """Enforce a destination inside the same grade and school.

        Runs on every create or write touching
        ``destination_grade_class_id`` or ``enrollment_id`` and
        delegates the test to ``_check_same_grade_school_condition``.
        This is what keeps a mutation a lateral move between classes
        instead of a grade change or a school transfer.

        :raises ValidationError: the destination class belongs to
            another grade or another school than the enrollment.
        """
        for record in self.sudo():
            if not record._check_same_grade_school_condition():
                error_message = (
                    _(
                        """
Context: Set class mutation destination
Database ID: %s
Problem: Destination Grade Class '%s' does not belong to the same
Grade/School as the enrollment
Solution: Select a Destination Grade Class within the same Grade and
School as the enrollment
"""
                    )
                    % (
                        record.id,
                        record.destination_grade_class_id.name,
                    )
                )
                raise ValidationError(error_message)

    def _check_same_grade_school_condition(self):
        """Return whether destination grade and school match.

        Extension point of the ``_check_same_grade_school`` constraint:
        override it to change the rule. A record still missing the
        destination class or the enrollment is accepted, otherwise both
        ``grade_id`` and ``school_id`` of
        ``destination_grade_class_id`` must equal those of
        ``enrollment_id``.

        :return: ``True`` when the combination is valid.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if not self.destination_grade_class_id or not self.enrollment_id:
            return True
        return (
            self.destination_grade_class_id.grade_id == self.enrollment_id.grade_id
            and self.destination_grade_class_id.school_id
            == self.enrollment_id.school_id
        )

    @api.constrains("state", "enrollment_id")
    def _check_enrollment_open(self):
        """Enforce an open enrollment once the document advances.

        Runs on every create or write touching ``state`` or
        ``enrollment_id`` and delegates the test to
        ``_check_enrollment_open_condition``, so a mutation cannot be
        confirmed or completed against an enrollment closed or
        cancelled in the meantime.

        :raises ValidationError: the document is ``confirm`` or ``done``
            while its enrollment is not ``open``.
        """
        for record in self.sudo():
            if not record._check_enrollment_open_condition():
                error_message = (
                    _(
                        """
Context: Change class mutation state into %s
Database ID: %s
Problem: Enrollment '%s' is not in open state
Solution: The enrollment must be open before this mutation can be
confirmed or completed
"""
                    )
                    % (
                        record.state,
                        record.id,
                        record.enrollment_id.name,
                    )
                )
                raise ValidationError(error_message)

    def _check_enrollment_open_condition(self):
        """Return whether the enrollment may still be mutated.

        Extension point of the ``_check_enrollment_open`` constraint:
        override it to change the rule. Documents outside ``confirm``
        and ``done`` are always accepted, so a draft may be prepared
        freely; in those two states ``enrollment_id.state`` must be
        ``open``.

        :return: ``True`` when the state combination is valid.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.state not in ("confirm", "done"):
            return True
        return self.enrollment_id.state == "open"

    @api.constrains("state", "enrollment_id")
    def _check_single_active_mutation(self):
        """Enforce a single live mutation per enrollment.

        Runs on every create or write touching ``state`` or
        ``enrollment_id`` and delegates the test to
        ``_check_single_active_mutation_condition``, preventing two
        competing documents from moving the same enrollment into
        different classes.

        :raises ValidationError: another draft or confirmed mutation
            already targets the same enrollment.
        """
        for record in self.sudo():
            if not record._check_single_active_mutation_condition():
                error_message = (
                    _(
                        """
Context: Change class mutation state into %s
Database ID: %s
Problem: Another mutation for enrollment '%s' is already draft or
waiting for approval
Solution: Complete, reject, or cancel the other mutation before
confirming this one
"""
                    )
                    % (
                        record.state,
                        record.id,
                        record.enrollment_id.name,
                    )
                )
                raise ValidationError(error_message)

    def _check_single_active_mutation_condition(self):
        """Return whether no rival mutation targets the enrollment.

        Extension point of the ``_check_single_active_mutation``
        constraint: override it to change the rule. Documents outside
        ``draft`` and ``confirm``, or without an enrollment, are always
        accepted; otherwise the search built by
        ``_get_single_active_mutation_criteria`` must come back empty.

        :return: ``True`` when no other mutation is pending.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.state not in ("draft", "confirm") or not self.enrollment_id:
            return True
        duplicate = self.search(
            self._get_single_active_mutation_criteria(),
        )
        return not duplicate

    def _get_single_active_mutation_criteria(self):
        """Return the domain finding rival mutation documents.

        Extension point of
        ``_check_single_active_mutation_condition``: override it to
        change what counts as a rival. Matches the other mutations (an
        ``id`` different from this one) on the same ``enrollment_id``
        whose state is ``draft`` or ``confirm``.

        :return: search domain for ``school_student_mutation``.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        return [
            ("id", "!=", self.id),
            ("enrollment_id", "=", self.enrollment_id.id),
            ("state", "in", ["draft", "confirm"]),
        ]

    @ssi_decorator.pre_done_check()
    def _10_check_ready(self):
        """Validate the mutation right before it turns done.

        ``pre_done_check`` hook fired by ``action_done`` while the
        document is still in ``confirm``, before the state moves to
        ``done`` and before ``_20_apply_mutation`` touches the
        enrollment. It replays two guards against live data: the
        enrollment must still be ``open`` and the destination class must
        still have a free seat.

        :raises ValueError: ``self`` is not a single record.
        :raises ValidationError: propagated from
            ``_check_done_enrollment_open`` or
            ``_check_done_destination_capacity``.
        """
        self.ensure_one()
        self._check_done_enrollment_open()
        self._check_done_destination_capacity()

    def _check_done_enrollment_open(self):
        """Refuse completion when the enrollment left the open state.

        Re-reads ``enrollment_id.state`` at completion time, because the
        enrollment may have been closed or cancelled after the mutation
        was approved; the user is then told to cancel the mutation
        instead of applying it.

        :raises ValueError: ``self`` is not a single record.
        :raises ValidationError: the enrollment is no longer ``open``.
        """
        self.ensure_one()
        if self.enrollment_id.state != "open":
            error_message = (
                _(
                    """
Context: Complete class mutation
Database ID: %s
Problem: Enrollment '%s' is no longer open
Solution: Cancel this mutation; the enrollment must stay open until
the mutation is completed
"""
                )
                % (
                    self.id,
                    self.enrollment_id.name,
                )
            )
            raise ValidationError(error_message)

    def _check_done_destination_capacity(self):
        """Refuse completion when the destination class is full.

        A destination class whose ``capacity`` is left at zero counts as
        unlimited and passes at once. Otherwise the open enrollments of
        ``destination_grade_class_id`` are counted through
        ``_get_destination_capacity_criteria`` and the mutation is
        rejected as soon as that count already reaches the capacity.

        :raises ValueError: ``self`` is not a single record.
        :raises ValidationError: the destination class has no seat left.
        """
        self.ensure_one()
        grade_class = self.destination_grade_class_id
        if not grade_class.capacity:
            return
        open_count = self.env["school_enrollment"].search_count(
            self._get_destination_capacity_criteria()
        )
        if open_count >= grade_class.capacity:
            error_message = (
                _(
                    """
Context: Complete class mutation
Database ID: %s
Problem: Destination Grade Class '%s' is at full capacity (%s/%s
students)
Solution: Choose a different destination class or increase its
capacity
"""
                )
                % (
                    self.id,
                    grade_class.name,
                    open_count,
                    grade_class.capacity,
                )
            )
            raise ValidationError(error_message)

    def _get_destination_capacity_criteria(self):
        """Return the domain counting seats taken in the destination.

        Extension point of ``_check_done_destination_capacity``:
        override it to change which enrollments consume a seat. Matches
        the enrollments of ``destination_grade_class_id`` in state
        ``open``.

        :return: search domain for ``school_enrollment``.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        return [
            ("grade_class_id", "=", self.destination_grade_class_id.id),
            ("state", "=", "open"),
        ]

    @ssi_decorator.post_done_action()
    def _20_apply_mutation(self):
        """Move the enrollment into the destination class.

        ``post_done_action`` hook fired by ``action_done`` once the
        document reached ``done``. It writes
        ``_prepare_mutation_enrollment_vals`` on ``enrollment_id`` as
        superuser, which cascades into ``school_student.grade_class_id``
        and into the enrolled counts of the source and destination
        Homerooms. Nothing reverts it, since ``done`` is terminal: an
        opposite mutation document is required to undo the move.

        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        self.enrollment_id.sudo().write(self._prepare_mutation_enrollment_vals())

    def _prepare_mutation_enrollment_vals(self):
        """Build the values written on the mutated enrollment.

        Points the enrollment at ``destination_grade_class_id`` and at
        ``destination_homeroom_id`` (``False`` when the destination
        class has no open batch), leaving grade, academic year and term,
        and billing untouched. Extension point: override it to carry
        more fields over to the enrollment.

        :return: dictionary of values for ``school_enrollment.write``.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        return {
            "grade_class_id": self.destination_grade_class_id.id,
            "homeroom_id": self.destination_homeroom_id.id or False,
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
