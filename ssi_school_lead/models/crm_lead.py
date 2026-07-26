# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

_SYNC_STUDENT_FAMILY_LINK_TRIGGER_FIELDS = [
    "partner_id",
    "student_id",
    "parent_relationship",
]


class CrmLead(models.Model):
    """
    Extends the CRM Lead model to associate leads with schools
    and prospective students for school admissions management.
    """

    _name = "crm.lead"
    _inherit = "crm.lead"
    _description = "CRM Lead"

    school_id = fields.Many2one(
        comodel_name="school",
        string="School",
        ondelete="restrict",
        help="The school associated with this lead.",
    )
    student_id = fields.Many2one(
        comodel_name="res.partner",
        string="Student",
        ondelete="restrict",
        domain=[("is_company", "=", False)],
        help="The prospective student associated with this lead.",
    )
    parent_relationship = fields.Selection(
        string="Parent Relationship",
        selection=[
            ("father", "Father"),
            ("mother", "Mother"),
            ("guardian", "Guardian"),
        ],
        help="Relationship of the parent/guardian contact to the prospective "
        "student. Used to link the student as a child or ward of the "
        "parent/guardian contact.",
    )
    admission_id = fields.Many2one(
        comodel_name="school_admission",
        string="Admission",
        ondelete="restrict",
        help="The school admission record created from this lead.",
    )
    create_admission_ok = fields.Boolean(
        string="Can Create Admission",
        compute="_compute_create_admission_ok",
        compute_sudo=True,
        help="Indicates whether an admission can still be created for this lead.",
    )
    parent_street = fields.Char(
        string="Parent Street",
        related="partner_id.street",
        store=True,
        help="Street address of the parent/guardian, mirrored from their contact record.",
    )
    parent_street2 = fields.Char(
        string="Parent Street2",
        related="partner_id.street2",
        store=True,
        help="Additional street address of the parent/guardian, mirrored from their "
        "contact record.",
    )
    parent_city = fields.Char(
        string="Parent City",
        related="partner_id.city",
        store=True,
        help="City of the parent/guardian, mirrored from their contact record.",
    )
    parent_state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="Parent State",
        related="partner_id.state_id",
        store=True,
        help="State/province of the parent/guardian, mirrored from their contact record.",
    )
    parent_zip = fields.Char(
        string="Parent Zip",
        related="partner_id.zip",
        store=True,
        help="Postal/zip code of the parent/guardian, mirrored from their contact record.",
    )
    parent_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Parent Country",
        related="partner_id.country_id",
        store=True,
        help="Country of the parent/guardian, mirrored from their contact record.",
    )
    parent_mobile = fields.Char(
        string="Parent Mobile",
        related="partner_id.mobile",
        store=True,
        help="Mobile number of the parent/guardian, mirrored from their contact record.",
    )
    parent_phone = fields.Char(
        string="Parent Phone",
        related="partner_id.phone",
        store=True,
        help="Phone number of the parent/guardian, mirrored from their contact record.",
    )
    parent_email = fields.Char(
        string="Parent Email",
        related="partner_id.email",
        store=True,
        help="Email address of the parent/guardian, mirrored from their contact record.",
    )

    @api.depends("admission_id")
    def _compute_create_admission_ok(self):
        for record in self:
            record.create_admission_ok = not record.admission_id

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._sync_student_family_link()
        return records

    def write(self, vals):
        res = super().write(vals)
        if any(field in vals for field in _SYNC_STUDENT_FAMILY_LINK_TRIGGER_FIELDS):
            self._sync_student_family_link()
        return res

    def _sync_student_family_link(self):
        for record in self:
            if not record.partner_id or not record.student_id:
                continue
            record.partner_id.sudo().link_child(
                record.student_id, record.parent_relationship
            )

    def action_create_admission(self):
        for record in self.sudo():
            result = record._create_admission()
        return result

    def _create_admission(self):
        self.ensure_one()
        if self.admission_id:
            return {
                "type": "ir.actions.act_window",
                "name": "Admission",
                "res_model": "school_admission",
                "res_id": self.admission_id.id,
                "view_mode": "form",
                "target": "current",
            }
        return {
            "type": "ir.actions.act_window",
            "name": "Create Admission",
            "res_model": "crm.lead.create_admission",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_lead_id": self.id,
                "default_school_id": self.school_id.id if self.school_id else False,
                "default_student_id": self.student_id.id if self.student_id else False,
            },
        }
