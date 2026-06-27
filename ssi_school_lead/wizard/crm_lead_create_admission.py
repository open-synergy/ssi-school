# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import api, fields, models


class CrmLeadCreateAdmission(models.TransientModel):
    _name = "crm.lead.create_admission"
    _description = "Wizard - Create Admission from CRM Lead"

    lead_id = fields.Many2one(
        string="Lead",
        comodel_name="crm.lead",
        required=True,
        readonly=True,
        help="The CRM lead this admission is created from.",
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=lambda r: datetime_date.today(),
        help="The date of the admission.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        required=True,
        help="The academic year for the admission.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=True,
        domain="[('year_id', '=', academic_year_id)]",
        help="The academic term for the admission.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        help="The school the student is being admitted to.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        help="Grade type derived from the selected school.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=True,
        domain="[('type_id', '=', grade_type_id)]",
        help="The grade level the student is being admitted to.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="res.partner",
        required=True,
        help="The student being admitted.",
    )

    @api.onchange("academic_year_id")
    def _onchange_academic_year_id(self):
        self.academic_term_id = False

    @api.onchange("school_id")
    def _onchange_school_id(self):
        self.grade_id = False

    def action_confirm(self):
        self.ensure_one()
        admission = self.env["school_admission"].create(self._prepare_admission_data())
        self.lead_id.sudo().write({"admission_id": admission.id})
        return {
            "type": "ir.actions.act_window",
            "name": "Admission",
            "res_model": "school_admission",
            "res_id": admission.id,
            "view_mode": "form",
            "target": "current",
        }

    def _prepare_admission_data(self):
        self.ensure_one()
        return {
            "date": self.date,
            "academic_year_id": self.academic_year_id.id,
            "academic_term_id": self.academic_term_id.id,
            "school_id": self.school_id.id,
            "grade_id": self.grade_id.id,
            "student_id": self.student_id.id,
            "currency_id": self.env.company.currency_id.id,
        }
