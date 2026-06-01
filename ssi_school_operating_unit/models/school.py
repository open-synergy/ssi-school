# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class School(models.Model):  # pylint: disable=too-few-public-methods
    """
    Extends the School model with multiple operating unit support,
    enabling operating unit-based data access control.
    """

    _name = "school"
    _inherit = [
        "school",
        "mixin.multiple_operating_unit",
    ]
