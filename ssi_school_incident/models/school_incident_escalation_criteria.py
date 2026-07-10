# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolIncidentEscalationCriteria(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents an explicit escalation criterion (Bab 8.7 of the YPII
    Incident & Parent Complaint Handling Guideline) used to decide whether
    a case must be escalated from one handling tier to the next, e.g. from
    Wali Kelas (Tier 1) to BK-Wakasek (Tier 2), or from BK-Wakasek to
    Kepala Sekolah (Tier 3).
    """

    _name = "school_incident_escalation_criteria"
    _inherit = ["mixin.master_data"]
    _description = "Incident Escalation Criteria"
    _order = "sequence asc, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help="Display and evaluation order of the escalation criterion. "
        "Lower values are evaluated/shown first.",
    )
    target_level = fields.Selection(
        string="Target Level",
        selection=[
            ("level_2", "Level 2 - Counselor/Vice Principal"),
            ("level_3", "Level 3 - Principal"),
        ],
        help="Handling tier the case must be escalated to when this "
        "criterion is met.",
    )
    verification_method = fields.Text(
        string="Verification Method",
        help="Description of how to verify that this escalation criterion "
        "has been met for a given incident case.",
    )
