# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolEnrollmentPaymentTermDetail(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a product/fee line detail on an actual enrollment payment term.
    Inherits mixin.product_line_account which provides standard product line fields
    such as name, account_id, uom_id, uom_quantity, price_unit, tax_ids,
    price_subtotal, price_tax, and price_total. If the term is linked to an invoice,
    each detail line will reference the corresponding invoice line (invoice_line_id)
    created when the invoice is generated.
    """

    _name = "school_enrollment_payment_term_detail"
    _description = "School Enrollment Payment Term Detail"
    _order = "sequence, product_category_id, product_id, id"
    _inherit = [
        "mixin.product_line_account",
    ]

    term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_enrollment_payment_term",
        ondelete="cascade",
        help="The enrollment payment term that owns this fee line.",
    )
    product_id = fields.Many2one(required=True)
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="term_id.enrollment_id.currency_id",
        store=True,
        required=False,
        help="The billing currency, automatically taken from the enrollment.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="term_id.enrollment_id.pricelist_id",
        store=True,
        help="The pricelist used, automatically taken from the enrollment.",
    )
    invoice_line_id = fields.Many2one(
        string="Invoice Line",
        comodel_name="account.move.line",
        readonly=True,
        ondelete="restrict",
        help=(
            "The invoice line linked to this detail, "
            "automatically populated when the invoice is generated."
        ),
    )

    def _prepare_invoice_line(self):
        self.ensure_one()
        aa = (  # pylint: disable=invalid-name,consider-using-ternary
            self.analytic_account_id and self.analytic_account_id.id or False
        )
        return {
            "product_id": self.product_id.id,
            "name": self.name,
            "account_id": self.account_id.id,
            "quantity": self.uom_quantity,
            "product_uom_id": self.uom_id.id,
            "price_unit": self.price_unit,
            "tax_ids": [(6, 0, self.tax_ids.ids)],
            "analytic_account_id": aa or False,
        }

    @api.model
    def create(self, vals):
        result = super().create(vals)
        enrollment = result.term_id.enrollment_id
        if enrollment:
            enrollment._recompute_product_summaries()  # pylint: disable=protected-access
        return result

    def write(self, vals):
        result = super().write(vals)
        self.mapped(
            "term_id.enrollment_id"
        )._recompute_product_summaries()  # pylint: disable=protected-access
        return result

    def unlink(self):
        enrollments = self.mapped("term_id.enrollment_id")
        result = super().unlink()
        enrollments._recompute_product_summaries()  # pylint: disable=protected-access
        return result
