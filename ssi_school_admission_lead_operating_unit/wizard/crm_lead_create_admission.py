# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class CrmLeadCreateAdmission(models.TransientModel):
    _name = "crm.lead.create_admission"
    _inherit = "crm.lead.create_admission"

    operating_unit_id = fields.Many2one(
        string="Operating Unit",
        comodel_name="operating.unit",
        help="Operating unit to assign to the created school admission.",
    )

    def action_confirm(self):
        self.ensure_one()
        res = super().action_confirm()
        if self.operating_unit_id and res.get("res_id"):
            self.env["school_admission"].browse(res["res_id"]).write(
                {"operating_unit_id": self.operating_unit_id.id}
            )
        return res
