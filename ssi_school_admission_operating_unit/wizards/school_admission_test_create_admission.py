# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class SchoolAdmissionTestCreateAdmission(models.TransientModel):
    _name = "school_admission_test.wizard_create_admission"
    _inherit = "school_admission_test.wizard_create_admission"

    def action_create_admission(self):
        self.ensure_one()
        res = super().action_create_admission()
        if self.admission_test_id.operating_unit_id and res.get("res_id"):
            self.env["school_admission"].browse(res["res_id"]).write(
                {"operating_unit_id": self.admission_test_id.operating_unit_id.id}
            )
        return res
