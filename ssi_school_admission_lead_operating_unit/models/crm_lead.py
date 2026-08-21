# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class CrmLead(models.Model):
    """
    Propagates the lead's operating unit into the admission wizards.
    Injects ``default_operating_unit_id`` into the context returned by
    the admission-creation actions, so both admission wizards open
    already defaulted to the lead's operating unit.
    """

    _name = "crm.lead"
    _inherit = "crm.lead"

    def action_create_admission(self):
        """Open the Create Admission wizard with the lead's OU defaulted.

        :return: an ``ir.actions.act_window`` dict opening
            ``crm.lead.create_admission``, with
            ``default_operating_unit_id`` added to its context
        """
        self.ensure_one()
        res = super().action_create_admission()
        if res.get("res_model") == "crm.lead.create_admission":
            context = res.get("context", {})
            context["default_operating_unit_id"] = self.operating_unit_id.id or False
            res["context"] = context
        return res

    def action_create_admission_form(self):
        """Open the Create Admission Form wizard, OU defaulted.

        :return: an ``ir.actions.act_window`` dict opening
            ``crm.lead.create_admission_form``, with
            ``default_operating_unit_id`` added to its context
        """
        self.ensure_one()
        res = super().action_create_admission_form()
        if res.get("res_model") == "crm.lead.create_admission_form":
            context = res.get("context", {})
            context["default_operating_unit_id"] = self.operating_unit_id.id or False
            res["context"] = context
        return res
