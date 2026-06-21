# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolEnrollmentProductSummary(models.Model):
    """
    Aggregates enrollment payment term details grouped by product.
    Each record represents the total quantity and amounts for one product
    across all payment terms of the parent enrollment.
    Records are maintained automatically whenever payment terms or their
    detail lines change.
    """

    _name = "school_enrollment.product_summary"
    _description = "School Enrollment - Product Summary"
    _order = "enrollment_id, product_id"

    enrollment_id = fields.Many2one(
        string="# Enrollment",
        comodel_name="school_enrollment",
        required=True,
        ondelete="cascade",
        help="The enrollment that owns this product summary line.",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
        help="The product/fee type being summarised across all payment terms.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="enrollment_id.currency_id",
        store=True,
        compute_sudo=True,
        help="The billing currency, taken from the enrollment.",
    )
    uom_quantity = fields.Float(
        string="Total Qty",
        digits="Product Unit of Measure",
        default=0.0,
        help="Sum of quantities for this product across all payment term details.",
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed Amount",
        currency_field="currency_id",
        default=0.0,
        help="Sum of untaxed subtotals for this product across all payment terms.",
    )
    amount_tax = fields.Monetary(
        string="Tax",
        currency_field="currency_id",
        default=0.0,
        help="Sum of tax amounts for this product across all payment terms.",
    )
    amount_total = fields.Monetary(
        string="Total",
        currency_field="currency_id",
        default=0.0,
        help="Sum of totals (including tax) for this product across all payment terms.",
    )
