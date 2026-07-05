# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolHomeroom(models.Model):
    """
    Extends School Homeroom with single operating unit support, and
    propagates the selected operating unit to every enrollment generated
    from this Homeroom batch.
    """

    _name = "school_homeroom"
    _inherit = [
        "school_homeroom",
        "mixin.single_operating_unit",
    ]

    def _prepare_enrollment_vals(self, student_id):
        res = super()._prepare_enrollment_vals(student_id)
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
