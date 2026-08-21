# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class SchoolAdmissionFormCreateAdmission(models.TransientModel):
    """Propagate the admission form's operating unit to the admission.

    Extends the Create Admission wizard so the ``school_admission`` it
    creates carries the same ``operating_unit_id`` as the source
    ``school_admission_form``.
    """

    _name = "school_admission_form.wizard_create_admission"
    _inherit = "school_admission_form.wizard_create_admission"

    def action_create_admission(self):
        """Confirm the wizard and stamp the OU on the new admission.

        Side effect: writes ``operating_unit_id`` on the
        ``school_admission`` record created by the base wizard, when
        the source admission form has one.

        :return: whatever the base ``action_create_admission`` returns
            (an ``ir.actions.act_window`` dict pointing at the new
            ``school_admission``)
        """
        self.ensure_one()
        res = super().action_create_admission()
        if self.admission_form_id.operating_unit_id and res.get("res_id"):
            self.env["school_admission"].browse(res["res_id"]).write(
                {"operating_unit_id": self.admission_form_id.operating_unit_id.id}
            )
        return res
