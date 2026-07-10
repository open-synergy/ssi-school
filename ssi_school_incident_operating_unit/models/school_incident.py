# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolIncident(models.Model):  # pylint: disable=too-few-public-methods
    """
    Extends School Incident with single operating unit support,
    restricting each incident case to one operating unit.
    """

    _name = "school_incident"
    _inherit = [
        "school_incident",
        "mixin.single_operating_unit",
    ]
