# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolAdmission(models.Model):  # pylint: disable=too-few-public-methods
    """
    Extends School Admission with single operating unit support
    for operating unit-based access and data segregation.
    """

    _name = "school_admission"
    _inherit = [
        "school_admission",
        "mixin.single_operating_unit",
    ]
