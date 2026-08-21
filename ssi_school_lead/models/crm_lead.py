# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

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
        readonly=False,
        help="Street address of the parent/guardian, mirrored from their contact record.",
    )
    parent_street2 = fields.Char(
        string="Parent Street2",
        related="partner_id.street2",
        store=True,
        readonly=False,
        help="Additional street address of the parent/guardian, mirrored from their "
        "contact record.",
    )
    parent_city = fields.Char(
        string="Parent City",
        related="partner_id.city",
        store=True,
        readonly=False,
        help="City of the parent/guardian, mirrored from their contact record.",
    )
    parent_state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="Parent State",
        related="partner_id.state_id",
        store=True,
        readonly=False,
        help="State/province of the parent/guardian, mirrored from their contact record.",
    )
    parent_zip = fields.Char(
        string="Parent Zip",
        related="partner_id.zip",
        store=True,
        readonly=False,
        help="Postal/zip code of the parent/guardian, mirrored from their contact record.",
    )
    parent_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Parent Country",
        related="partner_id.country_id",
        store=True,
        readonly=False,
        help="Country of the parent/guardian, mirrored from their contact record.",
    )
    parent_mobile = fields.Char(
        string="Parent Mobile",
        related="partner_id.mobile",
        store=True,
        readonly=False,
        help="Mobile number of the parent/guardian, mirrored from their contact record.",
    )
    parent_phone = fields.Char(
        string="Parent Phone",
        related="partner_id.phone",
        store=True,
        readonly=False,
        help="Phone number of the parent/guardian, mirrored from their contact record.",
    )
    parent_email = fields.Char(
        string="Parent Email",
        related="partner_id.email",
        store=True,
        readonly=False,
        help="Email address of the parent/guardian, mirrored from their contact record.",
    )
    student_nickname = fields.Char(
        string="Student Nickname",
        related="student_id.nickname",
        store=True,
        readonly=False,
        compute_sudo=True,
        help="Nickname of the prospective student, synchronized from the "
        "contact referenced by the Student field. Writing this field "
        "updates that contact's nickname.",
    )
    student_nisn = fields.Char(
        string="Student NISN",
        compute="_compute_student_nisn",
        compute_sudo=True,
        inverse="_inverse_student_nisn",
        search="_search_student_nisn",
        help="National student number (NISN) of the prospective student, "
        "read from and written to the contact referenced by the Student "
        "field. The value is never stored on the lead itself: it lives on "
        "that contact as an ID number record under the NISN category. "
        "Writing this field updates the contact even when the current user "
        "may not edit contact ID numbers directly. Emptying it archives "
        "the related ID number record instead of deleting it.",
    )

    @api.depends("student_id")
    def _compute_student_nisn(self):
        """Read the NISN of the contact referenced by ``student_id``.

        The contact is read with ``sudo()`` because ``res.partner`` and
        ``res.partner.id_number`` are only readable in full by the
        identification configurator groups, while admission officers must
        still see the number on the lead form.

        :return: nothing; assigns ``student_nisn``
        """
        for record in self:
            result = False
            if record.student_id:
                result = record.student_id.sudo().nisn
            record.student_nisn = result

    def _inverse_student_nisn(self):
        """Write ``student_nisn`` back onto the prospective student.

        The write goes through ``student_id.sudo()`` so that the NISN of
        the contact can be maintained from the lead form without granting
        the admission officer write access to ``res.partner`` or to
        ``res.partner.id_number``. The elevation is deliberately scoped to
        the student contact record, never to ``self``.

        An empty value on a lead without a student is a no-op, because the
        web client submits every editable non-stored field on save even
        when the lead has no prospective student yet.

        :raises UserError: when a non-empty NISN is set while
            ``student_id`` is empty
        :return: nothing; writes ``res.partner.nisn`` of the student
        """
        for record in self:
            if not record.student_id:
                if record.student_nisn:
                    error_message = (
                        _(
                            """
Context: Set Student NISN
Database ID: %s
Problem: No Student is selected on this lead
Solution: Select the Student first, then fill in the Student NISN
"""
                        )
                        % record.id
                    )
                    raise UserError(error_message)
                continue
            record.student_id.sudo().nisn = record.student_nisn

    def _search_student_nisn(self, operator, value):
        """Search leads by the NISN of their prospective student.

        The lookup is delegated to the ``search`` method of
        ``res.partner.nisn``, which resolves the NISN category on
        ``res.partner.id_number``.

        :param operator: the search operator supplied by the domain
        :param value: the NISN value being searched for
        :return: an Odoo search domain on ``crm.lead``
        """
        return [("student_id.nisn", operator, value)]

    @api.depends("admission_id")
    def _compute_create_admission_ok(self):
        """Allow creating an admission only while none exists yet.

        :return: nothing; assigns ``create_admission_ok``
        """
        for record in self:
            record.create_admission_ok = not record.admission_id

    @api.model_create_multi
    def create(self, vals_list):
        """Create leads, then sync the parent/student family link.

        Overridden so the same linkage performed on ``write()`` also
        runs for leads that are created with ``partner_id``,
        ``student_id``, and ``parent_relationship`` already set.

        :param vals_list: list of value dicts for the new leads
        :return: the created ``crm.lead`` recordset
        """
        records = super().create(vals_list)
        records._sync_student_family_link()
        return records

    def write(self, vals):
        """Write leads, then sync the parent/student family link.

        Overridden so changing ``partner_id``, ``student_id``, or
        ``parent_relationship`` keeps the student linked as a child/ward
        of the parent contact.

        :param vals: value dict being written
        :return: the same value ``write()`` normally returns
        """
        res = super().write(vals)
        if any(field in vals for field in _SYNC_STUDENT_FAMILY_LINK_TRIGGER_FIELDS):
            self._sync_student_family_link()
        return res

    def _sync_student_family_link(self):
        """Link the prospective student as a child/ward of the parent.

        Skips leads that have no parent contact or no student yet.
        The write goes through ``partner_id.sudo()`` so the admission
        officer does not need write access to ``res.partner`` family
        links.

        :return: nothing; writes ``res.partner`` family links
        """
        for record in self:
            if not record.partner_id or not record.student_id:
                continue
            record.partner_id.sudo().link_child(
                record.student_id, record.parent_relationship
            )

    def action_create_admission(self):
        """Open (or create) the admission for this lead.

        :return: an ``ir.actions.act_window`` dict, either opening the
            existing admission or the Create Admission wizard
        """
        for record in self.sudo():
            result = record._create_admission()
        return result

    def _create_admission(self):
        """Build the action that opens or creates this lead's admission.

        When ``admission_id`` is already set, the action opens that
        admission directly. Otherwise it opens the Create Admission
        wizard, prefilled with this lead's school and student.

        :return: an ``ir.actions.act_window`` dict
        """
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
