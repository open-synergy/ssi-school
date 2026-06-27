# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"

    def action_create_admission_form(self):
        self.ensure_one()
        res = super().action_create_admission_form()
        if res.get("res_model") == "crm.lead.create_admission_form":
            context = res.get("context", {})
            context["default_operating_unit_id"] = self.operating_unit_id.id or False
            res["context"] = context
        return res
