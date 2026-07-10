# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SchoolIncidentWizardEscalate(models.TransientModel):
    """
    Wizard that escalates a single school_incident case to a higher
    handling tier. Escalation is never automatic (v2.0 of the YPII
    Incident & Parent Complaint Handling Guideline, Bab 8.7): the user
    must select at least one school_incident_escalation_criteria record
    whose Target Level matches the tier being escalated to, and provide a
    narrative Escalation Reason. Every check is validated against the
    incident's escalate_ok policy field (state + group, configurable via
    Policy Template) before any change is applied.
    """

    _name = "school_incident.wizard_escalate"
    _description = "Escalate Incident to a Higher Handling Tier"

    incident_id = fields.Many2one(
        string="Incident",
        comodel_name="school_incident",
        required=True,
        readonly=True,
        help="The incident case being escalated.",
    )
    target_level = fields.Selection(
        string="Target Level",
        selection=[
            ("2", "Level 2 - Counselor/Vice Principal"),
            ("3", "Level 3 - Principal"),
        ],
        required=True,
        help="The handling tier this case will be escalated to.",
    )
    escalation_criteria_ids = fields.Many2many(
        string="Escalation Criteria",
        comodel_name="school_incident_escalation_criteria",
        relation="rel_school_incident_wizard_escalate_2_criteria",
        column1="wizard_id",
        column2="criteria_id",
        help=(
            "At least one criterion whose Target Level matches the "
            "selected Target Level above, justifying this escalation."
        ),
    )
    escalation_reason = fields.Text(
        string="Escalation Reason",
        required=True,
        help="Narrative/chronology explaining why this case is being escalated.",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get("active_model") == "school_incident":
            active_id = self.env.context.get("active_id")
            if active_id:
                res["incident_id"] = active_id
        return res

    def action_escalate_wizard(self):
        for record in self.sudo():
            record._escalate_wizard()  # pylint: disable=protected-access
        return {"type": "ir.actions.act_window_close"}

    def _escalate_wizard(self):
        self.ensure_one()
        if not self.incident_id.escalate_ok:
            error_message = (
                _(
                    """
Context: Escalate incident to a higher handling tier
Database ID: %s
Problem: Incident '%s' is not allowed to be escalated right now (check
state/policy)
Solution: Make sure the incident is Open and that you belong to a group
allowed by the escalate policy
"""
                )
                % (self.incident_id.id, self.incident_id.name)
            )
            raise UserError(error_message)
        self.incident_id.action_escalate(
            target_level=self.target_level,
            escalation_criteria_ids=self.escalation_criteria_ids,
            escalation_reason=self.escalation_reason,
        )
