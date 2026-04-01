# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolAdmissionFormTax(models.Model):
    """
    Represents a tax line computed from fee items in a school admission
    form, used for journal entry generation and tax reporting.
    """

    _name = "school_admission_form.tax"
    _description = "School Admission Form - Tax"
    _inherit = ["mixin.tax_line"]

    # account.move.line
    _partner_id_field_name = "partner_id"
    _analytic_account_id_field_name = "analytic_account_id"
    _label_field_name = "name"
    _amount_currency_field_name = "tax_amount"
    _normal_amount = "credit"

    admission_form_id = fields.Many2one(
        comodel_name="school_admission_form",
        string="# Admission Form",
        required=True,
        ondelete="cascade",
        help="The parent admission form this tax line belongs to.",
    )
    move_id = fields.Many2one(related="admission_form_id.move_id")
    currency_id = fields.Many2one(related="admission_form_id.currency_id")
    company_id = fields.Many2one(related="admission_form_id.company_id")
    company_currency_id = fields.Many2one(
        related="admission_form_id.company_currency_id"
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="admission_form_id.parent_id",
        help=(
            "The billing partner derived from the admission " "form's parent contact."
        ),
    )
    date = fields.Date(related="admission_form_id.date")
    # Additional
    account_move_line_id = fields.Many2one(
        string="Journal Item",
        comodel_name="account.move.line",
        copy=False,
        help=(
            "The journal entry line linked to this tax record "
            "after the form is posted."
        ),
    )
