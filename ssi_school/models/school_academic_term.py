# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class SchoolAcademicTerm(models.Model):
    _name = "school_academic_term"
    _inherit = ["mixin.master_data"]
    _description = "School Academic Term"
    _order = "year_id asc, date_start asc, id asc"

    date_start = fields.Date(
        string="Date Start",
        required=True,
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
    )
    year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        required=True,
        ondelete="restrict",
    )
    first_term = fields.Boolean(
        string="First Term of Academic Year?",
        compute="_compute_first_term",
        store=True,
        compute_sudo=True,
    )
    last_term = fields.Boolean(
        string="Last Term of Academic Year?",
        compute="_compute_last_term",
        store=True,
        compute_sudo=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Unstarted"),
            ("open", "On progress"),
            ("done", "Done"),
        ],
        default="draft",
    )
    enrollment_state = fields.Selection(
        string="Enrollment State",
        selection=[
            ("close", "Close"),
            ("open", "Open for Enrollment"),
        ],
        default="close",
        readonly=True,
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
