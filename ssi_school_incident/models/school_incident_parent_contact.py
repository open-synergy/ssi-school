# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import api, fields, models


class SchoolIncidentParentContact(models.Model):
    """
    Represents a single parent/guardian contact log entry for a School
    Incident case (YPII Incident & Parent Complaint Handling Guideline).
    Parent communication is central to case satisfaction, and a single
    case is often followed up through several contacts over time (e.g.
    an initial WhatsApp message, followed by a phone call, followed by
    a face-to-face meeting). This model keeps the full history of every
    contact instead of only the single "first contact" snapshot recorded
    directly on the incident (``school_incident.date_first_contact``),
    which is kept in sync from this log (see
    ``school_incident._sync_date_first_contact_from_parent_contact``).
    """

    _name = "school_incident_parent_contact"
    _description = "School Incident Parent Contact"
    _order = "contact_datetime"

    incident_id = fields.Many2one(
        string="# Incident",
        comodel_name="school_incident",
        required=True,
        ondelete="cascade",
        help="The incident case this parent contact log entry belongs to.",
    )
    contact_datetime = fields.Datetime(
        string="Contact Date & Time",
        required=True,
        default=lambda self: fields.Datetime.now(),
        help="Date and time this particular contact with the parent/guardian took place.",
    )
    contact_method = fields.Selection(
        string="Contact Method",
        selection=[
            ("whatsapp", "WhatsApp"),
            ("phone", "Phone"),
            ("face_to_face", "Face to Face"),
            ("letter", "Letter"),
        ],
        help="The channel used to make this particular contact.",
    )
    contacted_by_id = fields.Many2one(
        string="Contacted By",
        comodel_name="res.users",
        default=lambda self: self.env.user,
        help="The staff member who made this particular contact.",
    )
    parent_partner_id = fields.Many2one(
        string="Parent/Guardian Contact",
        comodel_name="res.partner",
        help=(
            "The parent or guardian contacted. Automatically defaulted "
            "from the incident's Parent/Guardian Contact when the "
            "Incident is selected, but can still be changed manually "
            "(e.g. when a different family member was reached)."
        ),
    )
    summary = fields.Text(
        string="Summary",
        required=True,
        help=(
            "Summary of what was communicated during this contact. "
            "Structure the note using the Empathy -> Facts -> Solution "
            "framework from the YPII Incident & Parent Complaint "
            "Handling Guideline: first acknowledge the parent's "
            "feelings (Empathy), then state the confirmed facts of the "
            "case (Facts), then describe the concrete resolution or "
            "next step offered (Solution)."
        ),
    )
    is_first_contact = fields.Boolean(
        string="First Contact",
        compute="_compute_is_first_contact",
        store=True,
        compute_sudo=True,
        help=(
            "True for the contact log entry with the earliest Contact "
            "Date & Time among all parent contact entries of the same "
            "incident; False for every other (later) entry."
        ),
    )

    @api.depends(
        "incident_id",
        "contact_datetime",
        "incident_id.parent_contact_ids.contact_datetime",
    )
    def _compute_is_first_contact(self):
        for record in self:
            contacts = record.incident_id.parent_contact_ids
            if not contacts:
                record.is_first_contact = False
                continue
            earliest = contacts.sorted(
                key=lambda contact: (
                    contact.contact_datetime or datetime.max,
                    contact.id,
                )
            )[:1]
            record.is_first_contact = record in earliest

    @api.onchange(
        "incident_id",
    )
    def onchange_parent_partner_id(self):
        self.parent_partner_id = False
        if self.incident_id:
            self.parent_partner_id = self.incident_id.parent_partner_id

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for vals, record in zip(vals_list, records):
            if not vals.get("parent_partner_id") and record.incident_id:
                record.parent_partner_id = record.incident_id.parent_partner_id
        records.mapped("incident_id")._sync_date_first_contact_from_parent_contact()
        return records

    def write(self, vals):
        incidents_before = self.mapped("incident_id")
        result = super().write(vals)
        incidents_after = self.mapped("incident_id")
        (
            incidents_before | incidents_after
        )._sync_date_first_contact_from_parent_contact()
        return result

    def unlink(self):
        incidents = self.mapped("incident_id")
        result = super().unlink()
        incidents._sync_date_first_contact_from_parent_contact()
        return result
