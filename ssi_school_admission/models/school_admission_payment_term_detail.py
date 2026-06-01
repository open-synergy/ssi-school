# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolAdmissionPaymentTermDetail(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a single fee line detail within a school admission
    payment term, specifying the product, amount, and associated
    journal entry line for one payment item.
    """

    _name = "school_admission_payment_term_detail"
    _description = "School Admission Payment Term Detail"
    _order = "sequence, product_category_id, product_id, id"
    _inherit = [
        "mixin.product_line_account",
    ]

    term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_admission_payment_term",
        ondelete="cascade",
        help="The parent payment term this detail line belongs to.",
    )
    product_id = fields.Many2one(required=True)
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="term_id.admission_id.currency_id",
        store=True,
        required=False,
        help="The currency derived from the parent admission record.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="term_id.admission_id.pricelist_id",
        store=True,
        help="The pricelist derived from the parent admission record.",
    )
    invoice_line_id = fields.Many2one(
        string="Invoice Line",
        comodel_name="account.move.line",
        readonly=True,
        ondelete="restrict",
        help=("The invoice line linked to this detail " "after the term is invoiced."),
    )

    def _prepare_invoice_line(self):
        self.ensure_one()
        aa = (
            self.analytic_account_id and self.analytic_account_id.id or False
        )  # pylint: disable=invalid-name,consider-using-ternary
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
