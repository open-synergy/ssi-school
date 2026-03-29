# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"
    _description = "CRM Lead"

    admission_form_id = fields.Many2one(
        string="Admission Form",
        comodel_name="school_admission_form",
        ondelete="restrict",
    )
    admission_test_id = fields.Many2one(
        string="Admission Test",
        comodel_name="school_admission_test",
        related="admission_form_id.admission_test_id",
        store=True,
        compute_sudo=True,
    )
    create_admission_form_ok = fields.Boolean(
        string="Can Create Admission Form",
        compute="_compute_create_admission_form_ok",
        compute_sudo=True,
    )

    @api.depends("admission_form_id")
    def _compute_create_admission_form_ok(self):
        for record in self:
            record.create_admission_form_ok = not record.admission_form_id

    def action_create_admission_form(self):
        self.ensure_one()
        if self.admission_form_id:
            return {
                "type": "ir.actions.act_window",
                "name": "Admission Form",
                "res_model": "school_admission_form",
                "res_id": self.admission_form_id.id,
                "view_mode": "form",
                "target": "current",
            }
        return {
            "type": "ir.actions.act_window",
            "name": "Create Admission Form",
            "res_model": "crm.lead.create_admission_form",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_lead_id": self.id,
                "default_school_id": self.school_id.id if self.school_id else False,
                "default_student_id": self.student_id.id if self.student_id else False,
            },
        }
