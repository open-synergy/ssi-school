# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class SchoolAdmissionPeriod(models.Model):
    _name = "school_admission_period"
    _inherit = ["mixin.master_data"]
    _description = "School Admission Period"
    _order = "term_id asc, date_start asc, id asc"

    date_start = fields.Date(
        string="Date Start",
        required=True,
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
    )
    term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=True,
        ondelete="restrict",
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
