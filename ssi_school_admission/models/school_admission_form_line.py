# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SchoolAdmissionFormLine(models.Model):
    """
    Represents a single fee line item within a school admission form,
    linked to a product and account for billing and journal entry
    generation.
    """

    _name = "school_admission_form.line"
    _inherit = [
        "mixin.product_line_account",
        "mixin.account_move_single_line_with_field",
    ]
    _description = "School Admission Form - Fee Line"
    _order = "admission_form_id, sequence"

    # Accounting Entry Mixin
    _move_id_field_name = "move_id"
    _account_id_field_name = "account_id"
    _partner_id_field_name = "partner_id"
    _analytic_account_id_field_name = "analytic_account_id"
    _currency_id_field_name = "currency_id"
    _company_currency_id_field_name = "company_currency_id"
    _amount_currency_field_name = "price_subtotal"
    _company_id_field_name = "company_id"
    _date_field_name = "date"
    _label_field_name = "name"
    _product_id_field_name = "product_id"
    _uom_id_field_name = "uom_id"
    _quantity_field_name = "uom_quantity"
    _price_unit_field_name = "price_unit"
    _normal_amount = "credit"

    admission_form_id = fields.Many2one(
        string="# Admission Form",
        comodel_name="school_admission_form",
        required=True,
        ondelete="cascade",
        help="The parent admission form this fee line belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help=("Determines the display order of this line " "on the admission form."),
    )
    pricelist_id = fields.Many2one(
        related="admission_form_id.pricelist_id",
        store=True,
        compute_sudo=True,
    )
    currency_id = fields.Many2one(
        related="admission_form_id.currency_id",
        store=True,
        compute_sudo=True,
    )
    product_id = fields.Many2one(
        required=True,
    )
    move_id = fields.Many2one(related="admission_form_id.move_id")
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

    @api.onchange(
        "allowed_pricelist_ids",
        "currency_id",
    )
    def onchange_pricelist_id(self):
        pass

    @api.onchange(
        "product_id",
    )
    def onchange_line_usage_id(self):
        self.usage_id = False  # pylint: disable=attribute-defined-outside-init
