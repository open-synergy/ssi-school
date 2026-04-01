# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolAdmissionPaymentTemplateTermDetail(models.Model):
    """
    Represents a single fee line within a school admission payment
    template term, specifying the product, quantity, price, and
    account for one fee item.
    """

    _name = "school_admission_payment_template.term.detail"
    _description = "School Admission Payment Template Term Detail"
    _order = "term_id, sequence, id"

    term_id = fields.Many2one(
        string="Term",
        comodel_name="school_admission_payment_template.term",
        ondelete="cascade",
        required=True,
        help="The parent payment template term this detail belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Determines the display order of this line within the term.",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
        change_default=True,
        help="The product representing the fee item for this line.",
    )
    name = fields.Char(
        string="Description",
        required=True,
        help="The description of this fee line item.",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
        help="The revenue account for posting this fee item.",
    )
    uom_quantity = fields.Float(
        string="Quantity",
        required=True,
        default=1.0,
        help="The quantity of the fee item.",
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="uom.uom",
        help="The unit of measure for the fee quantity.",
    )
    price_unit = fields.Float(
        string="Unit Price",
        help="The unit price of the fee item.",
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_sch_adm_pay_tmpl_term_detail_tax",
        column1="detail_id",
        column2="tax_id",
        help="The taxes applied to this fee line.",
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
