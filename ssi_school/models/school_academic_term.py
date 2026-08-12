# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolAcademicTerm(models.Model):
    """
    Represents a semester or term within an academic year.
    SchoolAcademicTerm is a sub-period of SchoolAcademicYear. Each term has two
    main states: state (Unstarted → On progress → Done) and enrollment_state
    (Close / Open for Enrollment). The term determines its position in the
    academic year via the first_term and last_term fields, automatically computed
    from SchoolAcademicYear's first_term_id / last_term_id. This position is used
    by SchoolEnrollment to decide whether to match the student's next_grade_id
    or current_grade_id.
    """

    _name = "school_academic_term"
    _inherit = ["mixin.master_data"]
    _description = "School Academic Term"
    _order = "year_id asc, date_start asc, id asc"

    date_start = fields.Date(
        string="Date Start",
        required=True,
        help="The first date of this semester/term.",
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
        help="The last date of this semester/term.",
    )
    year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        required=True,
        ondelete="restrict",
        help="The academic year that this semester/term belongs to.",
    )
    first_term = fields.Boolean(
        string="First Term of Academic Year?",
        compute="_compute_first_term",
        store=True,
        compute_sudo=True,
        help=(
            "Automatically set to True if this semester/term "
            "is the first within the academic year."
        ),
    )
    last_term = fields.Boolean(
        string="Last Term of Academic Year?",
        compute="_compute_last_term",
        store=True,
        compute_sudo=True,
        help=(
            "Automatically set to True if this semester/term "
            "is the last within the academic year."
        ),
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Unstarted"),
            ("open", "On progress"),
            ("done", "Done"),
        ],
        default="draft",
        help="Execution status of the semester/term: Unstarted, On Progress, or Done.",
    )
    enrollment_state = fields.Selection(
        string="Enrollment State",
        selection=[
            ("close", "Close"),
            ("open", "Open for Enrollment"),
        ],
        default="close",
        readonly=True,
        help="Student admission status: Closed or Open for Enrollment.",
    )

    @api.depends(
        "year_id",
        "year_id.first_term_id",
    )
    def _compute_first_term(self):
        """Flag the term that opens its academic year.

        ``first_term`` is ``True`` only for the record referenced by
        ``year_id.first_term_id``, that is the term with the earliest
        ``date_start`` of the year; every other term of the year gets
        ``False``. Enrollment uses this flag to decide whether students
        move up a grade or stay in the current one.
        """
        for record in self:
            result = False
            if record == record.year_id.first_term_id:
                result = True
            record.first_term = result

    @api.depends(
        "year_id",
        "year_id.last_term_id",
    )
    def _compute_last_term(self):
        """Flag the term that closes its academic year.

        ``last_term`` is ``True`` only for the record referenced by
        ``year_id.last_term_id``, that is the term with the latest
        ``date_start`` of the year; every other term gets ``False``.
        Enrollment uses this flag to decide whether a completed
        enrollment promotes the student to the next grade.
        """
        for record in self:
            result = False
            if record == record.year_id.last_term_id:
                result = True
            record.last_term = result

    @api.constrains("date_start", "date_end", "year_id")
    def _check_date_coherence(self):
        """Enforce term dates that are ordered and inside their year.

        Runs on every create or write touching ``date_start``,
        ``date_end`` or ``year_id``; records still missing one of the
        three pass untouched. Two rules are applied: ``date_end`` must
        be strictly later than ``date_start``, and the whole term range
        must stay inside the ``date_start`` / ``date_end`` range of
        ``year_id``.

        :raises ValidationError: the term ends before it starts, or the
            term range falls outside its academic year.
        """
        for record in self:
            if not (record.date_start and record.date_end and record.year_id):
                continue
            if record.date_end <= record.date_start:
                error_message = (
                    _(
                        """
Context: Set academic term dates
Database ID: %s
Problem: Date End must be after Date Start
Solution: Set Date End to a date later than Date Start
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
            year = record.year_id
            if record.date_start < year.date_start or record.date_end > year.date_end:
                error_message = (
                    _(
                        """
Context: Set academic term dates
Database ID: %s
Problem: Term dates fall outside the range of academic year '%s' (%s - %s)
Solution: Set term dates within the academic year's date range
"""
                    )
                    % (record.id, year.name, year.date_start, year.date_end)
                )
                raise ValidationError(error_message)

    def action_open(self):
        """Start the selected terms from the Start button.

        Calls ``_open`` as superuser on every record, so the user sees
        the status bar move from Unstarted to On progress. Nothing is
        returned and the client simply reloads the view.
        """
        for record in self.sudo():
            record._open()  # pylint: disable=protected-access

    def action_done(self):
        """Close the selected terms from the Done button.

        Calls ``_done`` as superuser on every record, so the user sees
        the status bar move to Done, marking the term as finished.
        Nothing is returned and the client simply reloads the view.
        """
        for record in self.sudo():
            record._done()  # pylint: disable=protected-access

    def action_restart(self):
        """Send the selected terms back to Unstarted.

        Calls ``_restart`` as superuser on every record, so a term
        started or closed by mistake returns to the ``draft`` state.
        Nothing is returned and the client simply reloads the view.
        """
        for record in self.sudo():
            record._restart()  # pylint: disable=protected-access

    def action_open_enrollment(self):
        """Open student admission for the selected terms.

        Calls ``_open_enrollment`` as superuser on every record, which
        switches ``enrollment_state`` to ``open`` so enrollments may be
        registered against the term. Nothing is returned and the client
        simply reloads the view.
        """
        for record in self.sudo():
            record._open_enrollment()  # pylint: disable=protected-access

    def action_close_enrollment(self):
        """Close student admission for the selected terms.

        Calls ``_close_enrollment`` as superuser on every record, which
        switches ``enrollment_state`` back to ``close`` so no further
        enrollment may be registered against the term. Nothing is
        returned and the client simply reloads the view.
        """
        for record in self.sudo():
            record._close_enrollment()  # pylint: disable=protected-access

    def _open(self):
        """Write ``state`` to ``open`` on a single term.

        Implementation behind ``action_open``, kept separate so other
        modules can extend the transition itself rather than the button.

        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        self.write(
            {
                "state": "open",
            }
        )

    def _done(self):
        """Write ``state`` to ``done`` on a single term.

        Implementation behind ``action_done``, kept separate so other
        modules can extend the transition itself rather than the button.

        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        self.write(
            {
                "state": "done",
            }
        )

    def _restart(self):
        """Write ``state`` back to ``draft`` on a single term.

        Implementation behind ``action_restart``, kept separate so other
        modules can extend the transition itself rather than the button.

        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        self.write(
            {
                "state": "draft",
            }
        )

    def _open_enrollment(self):
        """Write ``enrollment_state`` to ``open`` on a single term.

        Implementation behind ``action_open_enrollment``, kept separate
        so other modules can extend the transition itself rather than
        the button. It leaves ``state`` untouched: admission and
        execution status of the term are independent.

        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        self.write(
            {
                "enrollment_state": "open",
            }
        )

    def _close_enrollment(self):
        """Write ``enrollment_state`` to ``close`` on a single term.

        Implementation behind ``action_close_enrollment``, kept separate
        so other modules can extend the transition itself rather than
        the button. It leaves ``state`` untouched: admission and
        execution status of the term are independent.

        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        self.write(
            {
                "enrollment_state": "close",
            }
        )
