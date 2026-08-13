# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SchoolStudent(models.Model):
    """
    Represents a student's data in a school.
    A student is linked to a contact entity (res.partner) as the source
    of personal data.
    The system automatically tracks the student's current grade (current_grade_id)
    and next grade (next_grade_id) based on the enrollment history.
    The student's state reflects their actual status, ranging from waiting for
    enrollment, actively enrolled, on leave, suspended, graduated, transferred,
    dropped out, resigned, or deceased.
    """

    _name = "school_student"
    _inherit = ["mixin.master_data"]
    _description = "Student"

    contact_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
        help="The contact (partner) representing the personal data of this student.",
    )
    image_1920 = fields.Image(
        related="contact_id.image_1920",
        store=False,
        readonly=False,
        help="Student photo, taken from the linked contact record.",
    )
    street = fields.Char(
        related="contact_id.street",
        store=True,
        readonly=False,
        help="Street address of the student, synchronized from the contact.",
    )
    street2 = fields.Char(
        related="contact_id.street2",
        store=True,
        readonly=False,
        help="Second line of the student's address, synchronized from the contact.",
    )
    zip = fields.Char(
        related="contact_id.zip",
        store=True,
        readonly=False,
        help="Postal code of the student's address, synchronized from the contact.",
    )
    city_id = fields.Many2one(
        related="contact_id.city_id",
        store=True,
        readonly=False,
        help="City of the student's address, synchronized from the contact.",
    )
    state_id = fields.Many2one(
        related="contact_id.state_id",
        store=True,
        readonly=False,
        help="Province/state of the student's address, synchronized from the contact.",
    )
    country_id = fields.Many2one(
        related="contact_id.country_id",
        store=True,
        readonly=False,
        help="Country of the student's address, synchronized from the contact.",
    )
    phone = fields.Char(
        related="contact_id.phone",
        store=True,
        readonly=False,
        help="Phone number of the student, synchronized from the contact.",
    )
    mobile = fields.Char(
        related="contact_id.mobile",
        store=True,
        readonly=False,
        help="Mobile number of the student, synchronized from the contact.",
    )
    email = fields.Char(
        related="contact_id.email",
        store=True,
        readonly=False,
        help="Email address of the student, synchronized from the contact.",
    )

    # Personal Information
    gender = fields.Selection(
        related="contact_id.gender",
        store=True,
        readonly=False,
        help="Gender of the student, synchronized from the contact.",
    )
    birthdate_date = fields.Date(
        related="contact_id.birthdate_date",
        store=True,
        readonly=False,
        help="Date of birth of the student, synchronized from the contact.",
    )
    age = fields.Integer(
        related="contact_id.age",
        readonly=True,
        help="Current age of the student, computed live from the contact's date of birth.",
    )
    birth_city = fields.Char(
        related="contact_id.birth_city",
        store=True,
        readonly=False,
        help="City of birth of the student, synchronized from the contact.",
    )
    birth_state_id = fields.Many2one(
        related="contact_id.birth_state_id",
        store=True,
        readonly=False,
        help="State/province of birth of the student, synchronized from the contact.",
    )
    birth_country_id = fields.Many2one(
        related="contact_id.birth_country_id",
        store=True,
        readonly=False,
        help="Country of birth of the student, synchronized from the contact.",
    )
    nationality_id = fields.Many2one(
        related="contact_id.nationality_id",
        store=True,
        readonly=False,
        help="Nationality of the student, synchronized from the contact.",
    )
    blood_type = fields.Selection(
        related="contact_id.blood_type",
        store=True,
        readonly=False,
        help="ABO blood type of the student, synchronized from the contact.",
    )
    blood_type_rhesus = fields.Selection(
        related="contact_id.blood_type_rhesus",
        store=True,
        readonly=False,
        help="Rhesus blood type of the student, synchronized from the contact.",
    )
    religion_id = fields.Many2one(
        related="contact_id.religion_id",
        store=True,
        readonly=False,
        help="Religion of the student, synchronized from the contact.",
    )
    ethnicity_id = fields.Many2one(
        related="contact_id.ethnicity_id",
        store=True,
        readonly=False,
        help="Ethnicity of the student, synchronized from the contact.",
    )
    marital = fields.Selection(
        related="contact_id.marital",
        store=True,
        readonly=False,
        help="Marital status of the student, synchronized from the contact.",
    )

    # Bank Accounts
    bank_ids = fields.One2many(
        string="Bank Accounts",
        related="contact_id.bank_ids",
        readonly=False,
        help="Bank accounts of the student, managed through the linked contact.",
    )

    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        ondelete="restrict",
        help="The school where this student is enrolled.",
    )
    initial_grade_type_id = fields.Many2one(
        string="Initial Grade Type",
        related="school_id.grade_type_id",
        store=True,
        help=(
            "The initial grade type from the school, "
            "automatically populated from school data."
        ),
    )
    initial_grade_id = fields.Many2one(
        string="Initial Grade",
        comodel_name="school_grade",
        required=False,
        help=(
            "The student's class when first entering school "
            "before having any enrollment history."
        ),
    )
    current_grade_id = fields.Many2one(
        string="Current Grade",
        comodel_name="school_grade",
        compute="_compute_current_grade_id",
        store=True,
        compute_sudo=True,
        help=(
            "The student's current grade, automatically computed "
            "based on completed (done) enrollment history."
        ),
    )
    current_grade_type_id = fields.Many2one(
        string="Current Grade Type",
        related="current_grade_id.type_id",
        store=True,
        help=(
            "The grade type of the student's current grade, "
            "derived from the active grade."
        ),
    )
    next_grade_id = fields.Many2one(
        string="Next Grade",
        comodel_name="school_grade",
        related=False,
        compute="_compute_next_grade_id",
        store=True,
        compute_sudo=True,
        help=(
            "The next grade for the student, automatically computed "
            "based on grade ordering and last enrollment result."
        ),
    )
    enrollment_ids = fields.One2many(
        string="Enrollments",
        comodel_name="school_enrollment",
        inverse_name="student_id",
        readonly=True,
        help="The complete enrollment history of this student.",
    )
    active_enrollment_id = fields.Many2one(
        string="Active Enrollment",
        comodel_name="school_enrollment",
        compute="_compute_active_enrollment_id",
        store=True,
        compute_sudo=True,
        help="The currently active enrollment (status open) of this student.",
    )
    grade_class_id = fields.Many2one(
        string="Grade Class",
        comodel_name="school_grade_class",
        related="active_enrollment_id.grade_class_id",
        store=True,
        help="The student's active homeroom class, derived from the active enrollment.",
    )

    # Family
    father_id = fields.Many2one(
        string="Father",
        related="contact_id.father_id",
        store=True,
        readonly=False,
        domain=[("is_company", "=", False)],
        help="Contact data of the student's father.",
    )
    mother_id = fields.Many2one(
        string="Mother",
        related="contact_id.mother_id",
        store=True,
        readonly=False,
        domain=[("is_company", "=", False)],
        help="Contact data of the student's mother.",
    )
    guardian_id = fields.Many2one(
        string="Guardian",
        related="contact_id.guardian_id",
        store=True,
        readonly=False,
        domain=[("is_company", "=", False)],
        help="Contact data of the student's guardian if parents cannot be reached.",
    )

    # Transfer In
    is_transfer_in = fields.Boolean(
        string="Transfer In",
        help=(
            "Indicates that this student transferred in from another "
            "school, and may therefore be enrolled directly into any "
            "grade of any term, regardless of the computed current/next "
            "grade."
        ),
    )
    origin_school = fields.Char(
        string="Origin School",
        help="Name of the school this transfer-in student came from.",
    )
    transfer_date = fields.Date(
        string="Transfer Date",
        help="Date on which this student transferred in from the origin school.",
    )

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Waiting for Enrollment"),
            ("enrol", "Enrolled"),
            ("on_leave", "On Leave"),
            ("suspended", "Suspended"),
            ("graduate", "Graduated"),
            ("transferred", "Transferred Out"),
            ("dropped", "Dropped Out / Expelled"),
            ("resigned", "Resigned"),
            ("deceased", "Deceased"),
        ],
        default="draft",
        tracking=True,
        help=(
            "Current status of the student, from waiting for enrollment "
            "to actively enrolled, graduated, or exited."
        ),
    )

    # Maps each state to the set of states it may legally transition into
    # (including itself, so no-op writes are always allowed).
    #
    # "draft" (registration, not yet enrolled) and "enrol" (actively enrolled)
    # are the two normal churn states and may move to any other state directly
    # (mirrors existing accepted usage, e.g. withdrawing before ever attending).
    # Once a student reaches a terminal/exit state (graduate, transferred,
    # dropped, resigned, deceased), it must go through "draft" first before it
    # can be set back to "enrol" — this is the guard's real purpose: it blocks
    # nonsensical direct jumps like deceased -> enrol or graduate -> enrol.
    # "deceased" has no way out at all.
    _ALL_STATES = {
        "draft",
        "enrol",
        "on_leave",
        "suspended",
        "graduate",
        "transferred",
        "dropped",
        "resigned",
        "deceased",
    }
    _STATE_TRANSITIONS = {
        "draft": _ALL_STATES,
        "enrol": _ALL_STATES,
        "on_leave": {"on_leave", "enrol", "draft"},
        "suspended": {"suspended", "enrol", "draft", "dropped"},
        "graduate": {"graduate", "draft"},
        "transferred": {"transferred", "draft"},
        "dropped": {"dropped", "draft"},
        "resigned": {"resigned", "draft"},
        "deceased": {"deceased"},
    }

    def write(self, values):
        """Guard student state changes against illegal transitions.

        Overridden to enforce the ``_STATE_TRANSITIONS`` map before the
        data reaches the database: when ``values`` carries a ``state``,
        every record of ``self`` is tested and the whole write is
        refused unless the new state is reachable from the state the
        record currently holds. This blocks nonsensical jumps such as
        ``deceased`` to ``enrol`` or ``graduate`` to ``enrol``, which no
        button guard would catch when the write comes from data import
        or another module. Writes without ``state`` pass straight to the
        parent implementation.

        :param values: field values handed over to the parent ``write``.
        :return: result of the parent ``write``.
        :raises ValidationError: the requested state is not reachable
            from the current state of one of the records.
        """
        if values.get("state"):
            new_state = values["state"]
            state_labels = dict(self._fields["state"].selection)
            for record in self:
                allowed = self._STATE_TRANSITIONS.get(record.state, set())
                if new_state not in allowed:
                    error_message = (
                        _(
                            """
Context: Change student state
Database ID: %s
Problem: State cannot change from '%s' to '%s'
Solution: Follow the allowed student state transition sequence
"""
                        )
                        % (
                            record.id,
                            state_labels.get(record.state, record.state),
                            state_labels.get(new_state, new_state),
                        )
                    )
                    raise ValidationError(error_message)
        return super().write(values)

    @api.constrains("code", "school_id")
    def _check_duplicate_code(self):
        """Enforce a student code unique within its school.

        Runs on every create or write touching ``code`` or
        ``school_id``. The ``/`` placeholder is skipped, so any number
        of students may still be waiting for their number; any other
        code is counted with ``search_count`` among the other students
        of the same ``school_id`` and refused when already taken. The
        same code may therefore be reused in another school.

        :raises UserError: another student of the same school already
            uses this ``code``.
        """
        for record in self:
            if record.code == "/":
                continue
            criteria = [
                ("code", "=", record.code),
                ("id", "!=", record.id),
                ("code", "!=", "/"),
                ("school_id", "=", record.school_id.id),
            ]
            count_duplicate = self.search_count(criteria)
            if count_duplicate > 0:
                error_message = _(
                    """
Context: Create or update student
Database ID: %s
Problem: Duplicate code '%s' in school '%s'
Solution: Change the student code to be unique within the school
"""
                    % (record.id, record.code, record.school_id.name)
                )
                raise UserError(error_message)

    @api.depends("enrollment_ids", "enrollment_ids.state")
    def _compute_active_enrollment_id(self):
        """Point ``active_enrollment_id`` at the open enrollment.

        Filters ``enrollment_ids`` on state ``open`` and keeps the first
        match, since a student is expected to hold at most one open
        enrollment at a time; the field falls back to ``False`` when no
        enrollment is open. ``grade_class_id`` is related to this field,
        so the student's current class follows it.
        """
        for record in self:
            active_enrollment = record.enrollment_ids.filtered(
                lambda enrollment: enrollment.state == "open"
            )
            record.active_enrollment_id = (
                active_enrollment[:1].id if active_enrollment else False
            )

    @api.depends("initial_grade_id", "enrollment_ids", "enrollment_ids.state")
    def _compute_current_grade_id(self):
        """Derive the grade the student is sitting in right now.

        Searches the ``school_enrollment`` records of the student that
        are in state ``open`` or ``done``, sorts them by the
        ``date_start`` of their academic term (undated terms are sorted
        as 1900-01-01) and then by ``id``, and keeps the ``grade_id`` of
        the most recent one. A student without such an enrollment falls
        back to ``initial_grade_id``, the grade recorded when they first
        entered the school.
        """
        for record in self:
            result = record.initial_grade_id
            criteria = [
                ("state", "in", ["open", "done"]),
                ("student_id", "=", record.id),
            ]
            enrollments = (
                self.env["school_enrollment"]
                .search(criteria)
                .sorted(
                    key=lambda e: (
                        e.academic_term_id.date_start
                        or fields.Date.to_date("1900-01-01"),
                        e.id,
                    )
                )
            )
            if len(enrollments) > 0:
                result = enrollments[-1].grade_id
            record.current_grade_id = result

    @api.depends(
        "initial_grade_id",
        "enrollment_ids",
        "enrollment_ids.state",
        "school_id",
    )
    def _compute_next_grade_id(self):
        """Derive the grade the student should enroll into next.

        Three situations are handled. A student with neither
        ``initial_grade_id`` nor any enrollment is offered the lowest
        grade (smallest ``sequence``) of the ``grade_type_id`` of their
        school. A student with an ``initial_grade_id`` but still no
        enrollment is offered ``initial_grade_id.next_grade_id``. Once
        enrollments exist, the latest ``done`` enrollment, ordered by
        academic term ``date_start`` then ``id``, decides: when it
        closed the academic year (``last_term``) the student moves on to
        its ``promote_to_grade_id``, falling back to its ``grade_id``
        when no promotion was recorded; otherwise the student stays in
        that same ``grade_id``. The value is ``False`` when no rule
        applies.
        """
        for record in self:
            result = False
            if not record.initial_grade_id and not record.enrollment_ids:
                grade_type = record.school_id.grade_type_id
                result = (
                    self.env["school_grade"].search(
                        [("type_id", "=", grade_type.id)],
                        order="sequence asc, id",
                        limit=1,
                    )
                    if grade_type
                    else self.env["school_grade"]
                )
            elif record.initial_grade_id and not record.enrollment_ids:
                result = record.initial_grade_id.next_grade_id
            elif record.enrollment_ids:
                criteria = [
                    ("state", "=", "done"),
                    ("student_id", "=", record.id),
                ]
                enrollments = (
                    self.env["school_enrollment"]
                    .search(criteria)
                    .sorted(
                        key=lambda e: (
                            e.academic_term_id.date_start
                            or fields.Date.to_date("1900-01-01"),
                            e.id,
                        )
                    )
                )
                if len(enrollments) > 0:
                    last_enrollment = enrollments[-1]
                    if last_enrollment.last_term:
                        result = (
                            last_enrollment.promote_to_grade_id
                            or last_enrollment.grade_id
                        )
                    else:
                        result = last_enrollment.grade_id
            record.next_grade_id = result

    @api.onchange(
        "school_id",
    )
    def onchange_initial_grade_id(self):
        self.initial_grade_id = False

    def action_set_to_draft(self):
        """Send the selected students back to Waiting for Enrollment.

        Calls ``_set_to_draft`` as superuser on every record, which is
        also the only way out of an exit state such as Graduated or
        Dropped Out before a student may be enrolled again. Nothing is
        returned and the client simply reloads the view.
        """
        for record in self.sudo():
            record._set_to_draft()  # pylint: disable=protected-access

    def action_set_to_enroll(self):
        """Mark the selected students as actively enrolled.

        Calls ``_set_to_enroll`` as superuser on every record, so the
        status bar moves to Enrolled. The guard in ``write`` only
        accepts it from Waiting for Enrollment, On Leave or Suspended.
        Nothing is returned and the client simply reloads the view.
        """
        for record in self.sudo():
            record._set_to_enroll()  # pylint: disable=protected-access

    def action_set_to_on_leave(self):
        """Put the selected students on leave.

        Calls ``_set_to_on_leave`` as superuser on every record, so the
        status bar moves to On Leave for a student temporarily away but
        still expected back. Nothing is returned and the client simply
        reloads the view.
        """
        for record in self.sudo():
            record._set_to_on_leave()  # pylint: disable=protected-access

    def action_set_to_suspended(self):
        """Suspend the selected students.

        Calls ``_set_to_suspended`` as superuser on every record, so the
        status bar moves to Suspended; from there the student may only
        be re-enrolled, sent back to draft, or dropped out. Nothing is
        returned and the client simply reloads the view.
        """
        for record in self.sudo():
            record._set_to_suspended()  # pylint: disable=protected-access

    def action_set_to_graduate(self):
        """Mark the selected students as graduated.

        Calls ``_set_to_graduate`` as superuser on every record, moving
        the status bar to Graduated. This is an exit state: the student
        can only be sent back to Waiting for Enrollment afterwards.
        Nothing is returned and the client simply reloads the view.
        """
        for record in self.sudo():
            record._set_to_graduate()  # pylint: disable=protected-access

    def action_set_to_transferred(self):
        """Mark the selected students as transferred out.

        Calls ``_set_to_transferred`` as superuser on every record,
        moving the status bar to Transferred Out for a student who left
        for another school. This is an exit state: only a return to
        Waiting for Enrollment is allowed afterwards. Nothing is
        returned and the client simply reloads the view.
        """
        for record in self.sudo():
            record._set_to_transferred()  # pylint: disable=protected-access

    def action_set_to_dropped(self):
        """Mark the selected students as dropped out or expelled.

        Calls ``_set_to_dropped`` as superuser on every record, moving
        the status bar to Dropped Out / Expelled. This is an exit state:
        only a return to Waiting for Enrollment is allowed afterwards.
        Nothing is returned and the client simply reloads the view.
        """
        for record in self.sudo():
            record._set_to_dropped()  # pylint: disable=protected-access

    def action_set_to_resigned(self):
        """Mark the selected students as resigned.

        Calls ``_set_to_resigned`` as superuser on every record, moving
        the status bar to Resigned for a student who withdrew on their
        own. This is an exit state: only a return to Waiting for
        Enrollment is allowed afterwards. Nothing is returned and the
        client simply reloads the view.
        """
        for record in self.sudo():
            record._set_to_resigned()  # pylint: disable=protected-access

    def action_set_to_deceased(self):
        """Mark the selected students as deceased.

        Calls ``_set_to_deceased`` as superuser on every record, moving
        the status bar to Deceased. This state is final: the guard in
        ``write`` allows no transition out of it, so the action cannot
        be undone. Nothing is returned and the client simply reloads the
        view.
        """
        for record in self.sudo():
            record._set_to_deceased()  # pylint: disable=protected-access

    def _set_to_draft(self):
        """Write ``state`` to ``draft`` on a single student.

        Implementation behind ``action_set_to_draft``, kept separate so
        other modules can extend the transition itself. The write still
        goes through the guard in ``write``.

        :raises ValueError: ``self`` is not a single record.
        :raises ValidationError: the transition is rejected by ``write``.
        """
        self.ensure_one()
        self.write(
            {
                "state": "draft",
            }
        )

    def _set_to_enroll(self):
        """Write ``state`` to ``enrol`` on a single student.

        Implementation behind ``action_set_to_enroll``, kept separate so
        other modules can extend the transition itself. The write still
        goes through the guard in ``write``, which refuses it from any
        exit state.

        :raises ValueError: ``self`` is not a single record.
        :raises ValidationError: the transition is rejected by ``write``.
        """
        self.ensure_one()
        self.write(
            {
                "state": "enrol",
            }
        )

    def _set_to_on_leave(self):
        """Write ``state`` to ``on_leave`` on a single student.

        Implementation behind ``action_set_to_on_leave``, kept separate
        so other modules can extend the transition itself. The write
        still goes through the guard in ``write``.

        :raises ValueError: ``self`` is not a single record.
        :raises ValidationError: the transition is rejected by ``write``.
        """
        self.ensure_one()
        self.write(
            {
                "state": "on_leave",
            }
        )

    def _set_to_suspended(self):
        """Write ``state`` to ``suspended`` on a single student.

        Implementation behind ``action_set_to_suspended``, kept separate
        so other modules can extend the transition itself. The write
        still goes through the guard in ``write``.

        :raises ValueError: ``self`` is not a single record.
        :raises ValidationError: the transition is rejected by ``write``.
        """
        self.ensure_one()
        self.write(
            {
                "state": "suspended",
            }
        )

    def _set_to_graduate(self):
        """Write ``state`` to ``graduate`` on a single student.

        Implementation behind ``action_set_to_graduate``, kept separate
        so other modules can extend the transition itself. The write
        still goes through the guard in ``write``, which afterwards only
        allows a return to ``draft``.

        :raises ValueError: ``self`` is not a single record.
        :raises ValidationError: the transition is rejected by ``write``.
        """
        self.ensure_one()
        self.write(
            {
                "state": "graduate",
            }
        )

    def _set_to_transferred(self):
        """Write ``state`` to ``transferred`` on a single student.

        Implementation behind ``action_set_to_transferred``, kept
        separate so other modules can extend the transition itself. The
        write still goes through the guard in ``write``, which
        afterwards only allows a return to ``draft``.

        :raises ValueError: ``self`` is not a single record.
        :raises ValidationError: the transition is rejected by ``write``.
        """
        self.ensure_one()
        self.write(
            {
                "state": "transferred",
            }
        )

    def _set_to_dropped(self):
        """Write ``state`` to ``dropped`` on a single student.

        Implementation behind ``action_set_to_dropped``, kept separate
        so other modules can extend the transition itself. The write
        still goes through the guard in ``write``, which afterwards only
        allows a return to ``draft``.

        :raises ValueError: ``self`` is not a single record.
        :raises ValidationError: the transition is rejected by ``write``.
        """
        self.ensure_one()
        self.write(
            {
                "state": "dropped",
            }
        )

    def _set_to_resigned(self):
        """Write ``state`` to ``resigned`` on a single student.

        Implementation behind ``action_set_to_resigned``, kept separate
        so other modules can extend the transition itself. The write
        still goes through the guard in ``write``, which afterwards only
        allows a return to ``draft``.

        :raises ValueError: ``self`` is not a single record.
        :raises ValidationError: the transition is rejected by ``write``.
        """
        self.ensure_one()
        self.write(
            {
                "state": "resigned",
            }
        )

    def _set_to_deceased(self):
        """Write ``state`` to ``deceased`` on a single student.

        Implementation behind ``action_set_to_deceased``, kept separate
        so other modules can extend the transition itself. The write
        still goes through the guard in ``write``, which afterwards
        allows no transition at all: the state is final.

        :raises ValueError: ``self`` is not a single record.
        :raises ValidationError: the transition is rejected by ``write``.
        """
        self.ensure_one()
        self.write(
            {
                "state": "deceased",
            }
        )
