# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolIncidentType(models.Model):  # pylint: disable=too-few-public-methods
    """
    Represents a category/type of student incident or parent complaint
    (Bab 5 / Master Log kolom D of the YPII Incident & Parent Complaint
    Handling Guideline). Determines the default handling tier and the
    first-contact SLA that applies when a case of this type is logged.
    """

    _name = "school_incident_type"
    _inherit = ["mixin.master_data"]
    _description = "Incident Type"

    default_handling_level = fields.Selection(
        string="Default Handling Level",
        selection=[
            ("1", "Tier 1 - Homeroom Teacher"),
            ("2", "Tier 2 - Counselor/Vice Principal"),
            ("3", "Tier 3 - Principal"),
        ],
        help="Default handling tier assigned to incidents of this type: "
        "Tier 1 = Wali Kelas (Homeroom Teacher), "
        "Tier 2 = BK-Wakasek (Counselor/Vice Principal), "
        "Tier 3 = Kepala Sekolah (Principal). This is only the default; "
        "an actual incident case can still be escalated beyond this level.",
    )
    first_contact_sla_hour = fields.Float(
        string="First Contact SLA (Hour)",
        help="Maximum number of hours allowed, from the moment an incident "
        "of this type is logged, before the assigned handler must make "
        "first contact with the parties involved.",
    )
    is_health = fields.Boolean(
        string="Is Health-Related",
        help="Marks this incident type as health-related. Health-related "
        "incidents follow the separate Health Protocol SLA and escalation "
        "path defined outside this module, not the standard incident "
        "handling SLA configured here.",
    )
