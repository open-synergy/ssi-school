# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class CrmLeadCreateAdmission(models.TransientModel):
    """
    Extends the Create Admission wizard with an operating unit field.
    Lets the user pick (or default from the lead) the operating unit
    that the resulting ``school_admission`` record is assigned to.
    """

    _name = "crm.lead.create_admission"
    _inherit = "crm.lead.create_admission"

    operating_unit_id = fields.Many2one(
        string="Operating Unit",
        comodel_name="operating.unit",
        help="Operating unit to assign to the created school admission.",
    )

    def action_confirm(self):
        """Confirm the wizard and stamp the OU on the new admission.

        Side effect: writes ``operating_unit_id`` on the
        ``school_admission`` record created by the base wizard, when
        one was chosen on this wizard.

        :return: whatever the base ``action_confirm`` returns (an
            ``ir.actions.act_window`` dict pointing at the new
            ``school_admission``)
        """
        self.ensure_one()
        res = super().action_confirm()
        if self.operating_unit_id and res.get("res_id"):
            self.env["school_admission"].browse(res["res_id"]).write(
                {"operating_unit_id": self.operating_unit_id.id}
            )
        return res
