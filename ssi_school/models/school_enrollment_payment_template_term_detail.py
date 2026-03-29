# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolEnrollmentPaymentTemplateTermDetail(models.Model):
    _name = "school_enrollment_payment_template.term.detail"
    _description = "School Enrollment Payment Template Term Detail"
    _order = "term_id, sequence, id"

    term_id = fields.Many2one(
        string="Term",
        comodel_name="school_enrollment_payment_template.term",
        ondelete="cascade",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
        change_default=True,
    )
    name = fields.Char(
        string="Description",
        required=True,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
    )
    uom_quantity = fields.Float(
        string="Quantity",
        required=True,
        default=1.0,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="uom.uom",
    )
    price_unit = fields.Float(
        string="Unit Price",
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_school_enrollment_payment_template_term_detail_tax",
        column1="detail_id",
        column2="tax_id",
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
