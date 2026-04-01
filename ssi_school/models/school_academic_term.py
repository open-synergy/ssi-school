# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


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
        for record in self:
            result = False
            if record == record.year_id.last_term_id:
                result = True
            record.last_term = result

    def action_open(self):
        for record in self.sudo():
            record._open()

    def action_done(self):
        for record in self.sudo():
            record._done()

    def action_restart(self):
        for record in self.sudo():
            record._restart()

    def action_open_enrollment(self):
        for record in self.sudo():
            record._open_enrollment()

    def action_close_enrollment(self):
        for record in self.sudo():
            record._close_enrollment()

    def _open(self):
        self.ensure_one()
        self.write(
            {
                "state": "open",
            }
        )

    def _done(self):
        self.ensure_one()
        self.write(
            {
                "state": "done",
            }
        )

    def _restart(self):
        self.ensure_one()
        self.write(
            {
                "state": "draft",
            }
        )

    def _open_enrollment(self):
        self.ensure_one()
        self.write(
            {
                "enrollment_state": "open",
            }
        )

    def _close_enrollment(self):
        self.ensure_one()
        self.write(
            {
                "enrollment_state": "close",
            }
        )
