# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolAdmissionFormCreateAdmission(models.TransientModel):
    _name = "school_admission_form.wizard_create_admission"
    _description = "Create School Admission from Admission Form"

    admission_form_id = fields.Many2one(
        string="Admission Form",
        comodel_name="school_admission_form",
        required=True,
        readonly=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelists",
        comodel_name="product.pricelist",
        compute="_compute_allowed_pricelist_ids",
        store=False,
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=False,
    )
    payment_template_id = fields.Many2one(
        string="Payment Template",
        comodel_name="school_admission_payment_template",
        required=False,
    )
    receivable_journal_id = fields.Many2one(
        string="Receivable Journal",
        comodel_name="account.journal",
        required=False,
    )
    receivable_account_id = fields.Many2one(
        string="Receivable Account",
        comodel_name="account.account",
        required=False,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get("active_id")
        if active_id:
            res["admission_form_id"] = active_id
        return res

    @api.depends("currency_id")
    def _compute_allowed_pricelist_ids(self):
        Pricelist = self.env["product.pricelist"]  # pylint: disable=invalid-name
        for record in self:
            result = []
            if record.currency_id:
                criteria = [("currency_id", "=", record.currency_id.id)]
                result = Pricelist.search(criteria).ids
            record.allowed_pricelist_ids = result

    @api.onchange("currency_id")
    def _onchange_pricelist_id(self):
        self.pricelist_id = False

    def action_create_admission(self):
        self.ensure_one()
        form = self.admission_form_id
        SchoolAdmission = self.env["school_admission"]  # pylint: disable=invalid-name
        existing = SchoolAdmission.search(
            [("admission_form_id", "=", form.id)], limit=1
        )
        if existing:
            admission = existing
        else:
            admission = SchoolAdmission.create(
                {
                    "date": form.date,
                    "academic_year_id": form.academic_year_id.id,
                    "academic_term_id": form.academic_term_id.id,
                    "school_id": form.school_id.id,
                    "grade_id": form.grade_id.id,
                    "student_id": form.student_id.id,
                    "admission_form_id": form.id,
                    "admission_test_id": form.admission_test_id.id
                    if form.admission_test_id
                    else False,
                    "currency_id": self.currency_id.id,
                    "pricelist_id": self.pricelist_id.id
                    if self.pricelist_id
                    else False,
                    "payment_template_id": self.payment_template_id.id
                    if self.payment_template_id
                    else False,
                    "receivable_journal_id": self.receivable_journal_id.id
                    if self.receivable_journal_id
                    else False,
                    "receivable_account_id": self.receivable_account_id.id
                    if self.receivable_account_id
                    else False,
                }
            )
        return {
            "type": "ir.actions.act_window",
            "name": "School Admission",
            "res_model": "school_admission",
            "res_id": admission.id,
            "view_mode": "form",
            "target": "current",
        }
