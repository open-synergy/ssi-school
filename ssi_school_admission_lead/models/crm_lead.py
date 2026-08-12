# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLead(models.Model):  # pylint: disable=too-few-public-methods
    """
    Extends the CRM Lead model to link leads with school admission
    forms, supporting the admission process from a CRM opportunity.
    """

    _name = "crm.lead"
    _inherit = "crm.lead"
    _description = "CRM Lead"

    student_birthdate = fields.Date(
        string="Student Birthdate",
        related="student_id.birthdate_date",
        store=True,
        readonly=False,
        compute_sudo=True,
        help=(
            "Date of birth of the prospective student, synchronized from "
            "the contact referenced by the Student field. Writing this "
            "field updates the contact itself, so the identity data is not "
            "duplicated on the lead."
        ),
    )
    student_gender = fields.Selection(
        string="Student Gender",
        related="student_id.gender",
        store=True,
        readonly=False,
        compute_sudo=True,
        help=(
            "Gender of the prospective student, synchronized from the "
            "contact referenced by the Student field. Writing this field "
            "updates the contact itself, so the identity data is not "
            "duplicated on the lead."
        ),
    )
    birth_city = fields.Char(
        string="Birth City",
        related="student_id.birth_city",
        store=True,
        readonly=False,
        compute_sudo=True,
        help=(
            "City of birth of the prospective student, synchronized from "
            "the contact referenced by the Student field. Writing this "
            "field updates the contact itself, so the identity data is not "
            "duplicated on the lead."
        ),
    )
    religion_id = fields.Many2one(
        string="Religion",
        comodel_name="res_partner_religion",
        related="student_id.religion_id",
        store=True,
        readonly=False,
        compute_sudo=True,
        help=(
            "Religion of the prospective student, synchronized from the "
            "contact referenced by the Student field. Writing this field "
            "updates the contact itself, so the identity data is not "
            "duplicated on the lead."
        ),
    )
    nationality_id = fields.Many2one(
        string="Nationality",
        comodel_name="res.country",
        related="student_id.nationality_id",
        store=True,
        readonly=False,
        compute_sudo=True,
        help=(
            "Nationality of the prospective student, synchronized from the "
            "contact referenced by the Student field. Writing this field "
            "updates the contact itself, so the identity data is not "
            "duplicated on the lead."
        ),
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        help=(
            "Grade type derived from the selected school. Used to restrict "
            "the grades that can be selected on this lead."
        ),
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        ondelete="restrict",
        tracking=True,
        domain="[('type_id', '=', grade_type_id)]",
        help=(
            "The grade level the prospective student is applying for. "
            "Only grades belonging to the grade type of the selected "
            "school can be chosen."
        ),
    )
    admission_form_id = fields.Many2one(
        string="Admission Form",
        comodel_name="school_admission_form",
        ondelete="restrict",
        help=("The school admission form created from or linked " "to this lead."),
    )
    admission_test_id = fields.Many2one(
        string="Admission Test",
        comodel_name="school_admission_test",
        related="admission_form_id.admission_test_id",
        store=True,
        compute_sudo=True,
        help=(
            "The admission test linked to the associated "
            "admission form, populated automatically."
        ),
    )
    create_admission_form_ok = fields.Boolean(
        string="Can Create Admission Form",
        compute="_compute_create_admission_form_ok",
        compute_sudo=True,
        help=(
            "Indicates whether an admission form can still " "be created for this lead."
        ),
    )
    previous_school_id = fields.Many2one(
        string="Previous School",
        comodel_name="res.partner",
        tracking=True,
        help=(
            "The prospective student's previous school, restricted to the "
            "partners allowed by the company's Previous School "
            "configuration (see Allowed Previous Schools)."
        ),
    )
    allowed_previous_school_ids = fields.Many2many(
        string="Allowed Previous Schools",
        comodel_name="res.partner",
        compute="_compute_allowed_previous_school_ids",
        store=False,
        compute_sudo=True,
        help=(
            "Partners that can be selected on the Previous School field, "
            "computed from the company's Previous School Selection "
            "Method (manual/domain/code)."
        ),
    )

    @api.depends("admission_form_id")
    def _compute_create_admission_form_ok(self):
        """Flag the lead as still able to spawn an admission form.

        The value is ``True`` only while ``admission_form_id`` is empty:
        one lead owns at most one admission form, so once the form is
        linked the "Create Admission Form" button must stop offering to
        create a second one.
        """
        for record in self:
            record.create_admission_form_ok = not record.admission_form_id

    @api.depends(
        "company_id.previous_school_selection_method",
        "company_id.previous_school_ids",
        "company_id.previous_school_domain",
        "company_id.previous_school_python_code",
    )
    def _compute_allowed_previous_school_ids(self):
        """Resolve the partners selectable as the previous school.

        Delegates to ``mixin.many2one_configurator`` on the lead's
        company, so the result follows the company's Previous School
        Selection Method: the manual list, the stored domain, or the
        stored Python code. Leads without a company get an empty
        result, which lets the domain on ``previous_school_id`` block
        every partner rather than allow all of them.
        """
        for record in self:
            result = False
            if record.company_id:
                result = record.company_id._m2o_configurator_get_filter(
                    object_name="res.partner",
                    method_selection=(
                        record.company_id.previous_school_selection_method
                    ),
                    manual_recordset=record.company_id.previous_school_ids,
                    domain=record.company_id.previous_school_domain,
                    python_code=record.company_id.previous_school_python_code,
                )
            record.allowed_previous_school_ids = result

    def action_create_admission_form(self):
        """Open the admission form of this lead, or the wizard creating it.

        When the lead already has an ``admission_form_id``, the existing
        ``school_admission_form`` is opened in the main content area so
        the button never produces a duplicate document. Otherwise the
        ``crm.lead.create_admission_form`` wizard is opened as a dialog,
        pre-filled with this lead, its school and its student.

        :return: ``ir.actions.act_window`` dict
        """
        self.ensure_one()
        if self.admission_form_id:
            return {
                "type": "ir.actions.act_window",
                "name": "Admission Form",
                "res_model": "school_admission_form",
                "res_id": self.admission_form_id.id,
                "view_mode": "form",
                "target": "current",
            }
        return {
            "type": "ir.actions.act_window",
            "name": "Create Admission Form",
            "res_model": "crm.lead.create_admission_form",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_lead_id": self.id,
                "default_school_id": self.school_id.id if self.school_id else False,
                "default_student_id": self.student_id.id if self.student_id else False,
            },
        }

    def action_open_admission_test(self):
        """Open the admission test linked to this lead.

        ``admission_test_id`` is related to the admission form, so the
        button is only meaningful once that form has produced a
        ``school_admission_test``; it navigates to that test instead of
        creating anything.

        :return: ``ir.actions.act_window`` dict
        """
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Admission Test",
            "res_model": "school_admission_test",
            "res_id": self.admission_test_id.id,
            "view_mode": "form",
            "target": "current",
        }
