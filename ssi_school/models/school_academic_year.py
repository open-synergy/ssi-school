# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class SchoolAcademicYear(models.Model):
    _name = "school_academic_year"
    _inherit = ["mixin.master_data"]
    _description = "School Academic Year"
    _order = "date_start asc, id asc"

    date_start = fields.Date(
        string="Date Start",
        required=True,
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
    )
    term_ids = fields.One2many(
        string="Terms",
        comodel_name="school_academic_term",
        inverse_name="year_id",
        readonly=True,
    )
    first_term_id = fields.Many2one(
        string="First Term",
        comodel_name="school_academic_term",
        compute="_compute_first_last_term",
        store=True,
        compute_sudo=True,
    )
    last_term_id = fields.Many2one(
        string="Last Term",
        comodel_name="school_academic_term",
        compute="_compute_first_last_term",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "term_ids",
    )
    def _compute_first_last_term(self):
        for record in self:
            first_term = last_term = False
            if record.term_ids:
                first_term = record.term_ids[0]
                last_term = record.term_ids[-1]
            record.first_term_id = first_term
            record.last_term_id = last_term
