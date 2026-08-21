# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import api, fields, models


class CrmLeadCreateAdmissionForm(models.TransientModel):
    """Collects the data needed to turn a CRM lead into an admission form.

    The lead alone does not carry everything a ``school_admission_form``
    requires (academic year and term, parent, pricelist, fee template),
    so this dialog gathers the missing values, creates the document and
    links it back to the originating lead.
    """

    _name = "crm.lead.create_admission_form"
    _description = "Wizard - Create Admission Form from CRM Lead"

    lead_id = fields.Many2one(
        string="Lead",
        comodel_name="crm.lead",
        required=True,
        readonly=True,
        help="The CRM lead this admission form is created from.",
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=lambda r: datetime_date.today(),
        help="The date of the admission form.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        required=True,
        help="The academic year for the admission form.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=True,
        domain="[('year_id', '=', academic_year_id), ('is_open_admission', '=', True)]",
        help=(
            "The academic term for the admission form. "
            "Only terms open for admission are shown."
        ),
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        help="The school the student is applying to.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=True,
        domain="[('type_id', '=', grade_type_id)]",
        help="The grade level the student is applying for.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="res.partner",
        required=True,
        help="The student submitting the admission form.",
    )
    parent_id = fields.Many2one(
        string="Parent",
        comodel_name="res.partner",
        required=True,
        help="The parent or guardian of the student.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=True,
        help="The pricelist applied to the admission fees.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        help="Grade type derived from the selected school.",
    )
    fee_template_id = fields.Many2one(
        string="Fee Template",
        comodel_name="school_admission_fee_template",
        required=False,
        help=(
            "The fee template to apply to the admission form. "
            "Auto-populated based on school and grade."
        ),
    )

    @api.model
    def default_get(self, fields_list):
        """Pre-fill the academic term and year with the open admission term.

        Overridden because the caller's context only carries the lead,
        its school and its student. The earliest ``school_academic_term``
        flagged ``is_open_admission`` is looked up and used to seed
        ``academic_term_id`` and ``academic_year_id``, but only when the
        caller did not already provide them.

        :param fields_list: field names the client asks defaults for
        :return: dict of default values
        """
        res = super().default_get(fields_list)
        AcademicTerm = self.env["school_academic_term"]  # pylint: disable=invalid-name
        term = AcademicTerm.search(
            [("is_open_admission", "=", True)],
            limit=1,
            order="date_start asc",
        )
        if term:
            if "academic_term_id" not in res or not res.get("academic_term_id"):
                res["academic_term_id"] = term.id
            if "academic_year_id" not in res or not res.get("academic_year_id"):
                res["academic_year_id"] = term.year_id.id
        return res

    @api.onchange("academic_year_id")
    def onchange_academic_year_id(self):
        if self.academic_term_id.year_id != self.academic_year_id:
            self.academic_term_id = False

    @api.onchange("school_id")
    def onchange_school_id(self):
        self.grade_id = False
        self.fee_template_id = False

    # NOTE: kept as `_onchange_grade_id` (not `onchange_grade_id`). The
    # target name collides with an unrelated onchange method of the same
    # name in ssi_school_admission/models/school_admission_test.py; the
    # Design Decision of issue #330 forbids renaming when another module
    # carries a same-named referent. See .validator-exceptions.
    @api.onchange("grade_id")
    def _onchange_grade_id(self):
        self.fee_template_id = False

    def action_confirm(self):
        """Create the admission form and open it.

        Side effects: a ``school_admission_form`` is created from the
        wizard values, and the originating lead is written (in ``sudo``)
        so its ``admission_form_id`` points at that new document. When a
        fee template is chosen, its journal and account are copied onto
        the admission form as well.

        :return: ``ir.actions.act_window`` dict opening the new form
        """
        self.ensure_one()
        vals = {
            "date": self.date,
            "academic_year_id": self.academic_year_id.id,
            "academic_term_id": self.academic_term_id.id,
            "school_id": self.school_id.id,
            "grade_id": self.grade_id.id,
            "student_id": self.student_id.id,
            "parent_id": self.parent_id.id,
            "pricelist_id": self.pricelist_id.id,
            "currency_id": self.pricelist_id.currency_id.id,
        }
        if self.fee_template_id:
            vals["fee_template_id"] = self.fee_template_id.id
            vals["journal_id"] = self.fee_template_id.journal_id.id or False
            vals["account_id"] = self.fee_template_id.account_id.id or False
        admission_form = self.env["school_admission_form"].create(vals)
        self.lead_id.sudo().write(
            {"admission_form_id": admission_form.id}
        )  # pylint: disable=no-member
        return {
            "type": "ir.actions.act_window",
            "name": "Admission Form",
            "res_model": "school_admission_form",
            "res_id": admission_form.id,  # pylint: disable=no-member
            "view_mode": "form",
            "target": "current",
        }
