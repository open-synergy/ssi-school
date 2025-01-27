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
