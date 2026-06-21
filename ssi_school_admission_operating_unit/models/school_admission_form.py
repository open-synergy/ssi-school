# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolAdmissionForm(models.Model):
    """
    Extends School Admission Form with single operating unit support
    for operating unit-based access and data segregation.
    Propagates operating_unit_id to the generated accounting entry.
    """

    _name = "school_admission_form"
    _inherit = [
        "school_admission_form",
        "mixin.single_operating_unit",
    ]

    def _prepare_standard_move(self):
        res = super()._prepare_standard_move()
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
