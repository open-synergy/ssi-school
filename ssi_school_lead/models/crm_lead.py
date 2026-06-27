# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLead(models.Model):
    """
    Extends the CRM Lead model to associate leads with schools
    and prospective students for school admissions management.
    """

    _name = "crm.lead"
    _inherit = "crm.lead"
    _description = "CRM Lead"

    school_id = fields.Many2one(
        comodel_name="school",
        string="School",
        ondelete="restrict",
        help="The school associated with this lead.",
    )
    student_id = fields.Many2one(
        comodel_name="res.partner",
        string="Student",
        ondelete="restrict",
        help="The prospective student associated with this lead.",
    )
    admission_id = fields.Many2one(
        comodel_name="school_admission",
        string="Admission",
        ondelete="restrict",
        help="The school admission record created from this lead.",
    )
    create_admission_ok = fields.Boolean(
        string="Can Create Admission",
        compute="_compute_create_admission_ok",
        compute_sudo=True,
        help="Indicates whether an admission can still be created for this lead.",
    )

    @api.depends("admission_id")
    def _compute_create_admission_ok(self):
        for record in self:
            record.create_admission_ok = not record.admission_id

    def action_create_admission(self):
        for record in self.sudo():
            result = record._create_admission()
        return result

    def _create_admission(self):
        self.ensure_one()
        if self.admission_id:
            return {
                "type": "ir.actions.act_window",
                "name": "Admission",
                "res_model": "school_admission",
                "res_id": self.admission_id.id,
                "view_mode": "form",
                "target": "current",
            }
        return {
            "type": "ir.actions.act_window",
            "name": "Create Admission",
            "res_model": "crm.lead.create_admission",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_lead_id": self.id,
                "default_school_id": self.school_id.id if self.school_id else False,
                "default_student_id": self.student_id.id if self.student_id else False,
            },
        }
