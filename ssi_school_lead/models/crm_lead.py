# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"
    _description = "CRM Lead"

    school_id = fields.Many2one(
        comodel_name="school",
        string="School",
        ondelete="restrict",
    )
    student_id = fields.Many2one(
        comodel_name="res.partner",
        string="Student",
        ondelete="restrict",
    )
