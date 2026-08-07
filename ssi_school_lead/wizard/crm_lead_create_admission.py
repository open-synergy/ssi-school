# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import api, fields, models


class CrmLeadCreateAdmission(models.TransientModel):
    """
    Wizard that creates the school_admission for a CRM lead's
    prospective student, deriving the payment template (and, through
    it, the receivable journal/account and customer invoice settings)
    from the selected school, grade, and academic term.
    """

    _name = "crm.lead.create_admission"
    _description = "Wizard - Create Admission from CRM Lead"

    lead_id = fields.Many2one(
        string="Lead",
        comodel_name="crm.lead",
        required=True,
        readonly=True,
        help="The CRM lead this admission is created from.",
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=lambda r: datetime_date.today(),
        help="The date of the admission.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        required=True,
        help="The academic year for the admission.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=True,
        domain="[('year_id', '=', academic_year_id), ('is_open_admission', '=', True)]",
        help="The academic term for the admission. Only terms open for admission are shown.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        help="The school the student is being admitted to.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        help="Grade type derived from the selected school.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=True,
        domain="[('type_id', '=', grade_type_id)]",
        help="The grade level the student is being admitted to.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="res.partner",
        required=True,
        help="The student being admitted.",
    )
    payment_template_id = fields.Many2one(
        string="Payment Template",
        comodel_name="school_admission_payment_template",
        required=False,
        help=(
            "The payment template to apply to the admission. "
            "Auto-populated based on school, grade, and academic term."
        ),
    )

    @api.model
    def default_get(self, fields_list):
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
    def _onchange_academic_year_id(self):
        if self.academic_term_id.year_id != self.academic_year_id:
            self.academic_term_id = False

    @api.onchange("school_id")
    def _onchange_school_id(self):
        self.grade_id = False

    @api.onchange("school_id", "grade_id", "academic_term_id")
    def _onchange_payment_template_id(self):
        self.payment_template_id = False
        if self.school_id and self.grade_id and self.academic_term_id:
            PaymentTemplate = self.env[  # pylint: disable=invalid-name
                "school_admission_payment_template"
            ]
            criteria = [
                ("school_id", "=", self.school_id.id),
                ("grade_id", "=", self.grade_id.id),
                ("academic_term_id", "=", self.academic_term_id.id),
            ]
            template = PaymentTemplate.search(criteria, limit=1)
            if template:
                self.payment_template_id = template

    def action_confirm(self):
        self.ensure_one()
        admission = self.env["school_admission"].create(self._prepare_admission_data())
        self.lead_id.sudo().write(
            {
                "admission_id": admission.id,
                "student_id": self.student_id.id,
            }
        )
        if self.payment_template_id:
            admission.action_compute_payment()
        return {
            "type": "ir.actions.act_window",
            "name": "Admission",
            "res_model": "school_admission",
            "res_id": admission.id,
            "view_mode": "form",
            "target": "current",
        }

    def _prepare_admission_data(self):
        """Build the ``school_admission`` values for this wizard.

        ``customer_invoice_type_id`` and ``auto_confirm_customer_invoice``
        are copied straight from ``payment_template_id``, mirroring the
        ``receivable_journal_id``/``receivable_account_id`` conditional
        pattern below: this wizard exposes no override field for either
        of the four, so the template is the only source of truth.

        :return: dict of ``school_admission`` values
        """
        self.ensure_one()
        return {
            "date": self.date,
            "academic_year_id": self.academic_year_id.id,
            "academic_term_id": self.academic_term_id.id,
            "school_id": self.school_id.id,
            "grade_id": self.grade_id.id,
            "student_id": self.student_id.id,
            "currency_id": self.env.company.currency_id.id,
            "payment_template_id": self.payment_template_id.id
            if self.payment_template_id
            else False,
            "receivable_journal_id": self.payment_template_id.receivable_journal_id.id
            if self.payment_template_id
            else False,
            "receivable_account_id": self.payment_template_id.receivable_account_id.id
            if self.payment_template_id
            else False,
            "customer_invoice_type_id": (
                self.payment_template_id.customer_invoice_type_id.id
                if self.payment_template_id
                else False
            ),
            "auto_confirm_customer_invoice": (
                self.payment_template_id.auto_confirm_customer_invoice
                if self.payment_template_id
                else False
            ),
        }
