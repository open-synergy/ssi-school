# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolIncidentWeeklyReview(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Extends School Incident Weekly Review with single operating unit
    support, restricting each weekly case review to one operating unit.
    """

    _name = "school_incident_weekly_review"
    _inherit = [
        "school_incident_weekly_review",
        "mixin.single_operating_unit",
    ]
