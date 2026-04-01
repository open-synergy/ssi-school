# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolEnrollmentPaymentTemplateTermDetail(models.Model):
    """
    Represents a product/fee line detail within a payment template term.
    Each detail line defines one fee type or product to be billed, including
    the financial account, quantity, unit price, and applicable taxes.
    When a product is selected, the name and income account are populated
    automatically via onchange.
    """

    _name = "school_enrollment_payment_template.term.detail"
    _description = "School Enrollment Payment Template Term Detail"
    _order = "term_id, sequence, id"

    term_id = fields.Many2one(
        string="Term",
        comodel_name="school_enrollment_payment_template.term",
        ondelete="cascade",
        required=True,
        help="The template payment period that owns this fee line.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Order of the line within the payment period. Lower values appear first.",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
        change_default=True,
        help="The product or fee type to be billed.",
    )
    name = fields.Char(
        string="Description",
        required=True,
        help=(
            "Description or label of the fee. "
            "Automatically populated from the product name."
        ),
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
        help=(
            "The income account for recording this billing line. "
            "Automatically populated from the product's income account."
        ),
    )
    uom_quantity = fields.Float(
        string="Quantity",
        required=True,
        default=1.0,
        help="Quantity or number of units to be billed.",
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="uom.uom",
        help=(
            "Unit of measure for the billing quantity. "
            "Automatically populated from the product's unit."
        ),
    )
    price_unit = fields.Float(
        string="Unit Price",
        help="Unit price per unit of the product/fee to be billed.",
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_school_enrollment_payment_template_term_detail_tax",
        column1="detail_id",
        column2="tax_id",
        help="Taxes applied to this billing line.",
    )

    @api.onchange("product_id")
    def onchange_name(self):
        if self.product_id:
            self.name = self.product_id.name
            if self.product_id.uom_id:
                self.uom_id = self.product_id.uom_id

    @api.onchange("product_id")
    def onchange_account_id(self):
        if self.product_id and self.product_id.property_account_income_id:
            self.account_id = self.product_id.property_account_income_id
