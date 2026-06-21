# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolAdmissionProductSummary(models.Model):
    """
    Aggregates payment term detail lines across all terms in a school
    admission, grouped by product. Recomputed automatically whenever
    term or term detail records are created, modified, or deleted.
    """

    _name = "school_admission_product_summary"
    _description = "School Admission Product Summary"
    _order = "sequence, product_id, id"

    admission_id = fields.Many2one(
        string="Admission",
        comodel_name="school_admission",
        ondelete="cascade",
        help="The parent school admission this summary line belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        help="Display order of this product summary line.",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
        ondelete="restrict",
        help="The product whose amounts are aggregated across all payment terms.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="admission_id.currency_id",
        store=True,
        help="The currency derived from the parent admission record.",
    )
    amount_untaxed = fields.Monetary(
        string="Subtotal",
        currency_field="currency_id",
        help="Total amount before taxes for this product across all terms.",
    )
    amount_tax = fields.Monetary(
        string="Tax",
        currency_field="currency_id",
        help="Total tax amount for this product across all terms.",
    )
    amount_total = fields.Monetary(
        string="Total",
        currency_field="currency_id",
        help="Total amount including taxes for this product across all terms.",
    )
