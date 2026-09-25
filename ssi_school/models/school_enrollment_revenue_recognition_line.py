# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolEnrollmentRevenueRecognitionLine(models.Model):
    """
    One balanced debit/credit pair posted for one invoiced payment term
    detail, moving its already-billed amount from the temporary account
    used on the customer invoice line to the detail's own Final
    Account. One record is generated per invoiced
    ``school_enrollment_payment_term_detail`` that carries a Final
    Account different from the account already used on its own
    customer invoice line, so an enrollment billed across several terms
    and accounts produces one Recognition Line per originating detail.
    Debit and credit journal item creation is delegated to the
    inherited ``mixin.account_move_double_line``; this model itself
    only carries the values (both accounts, amount, and the involved
    partner/analytic account) that mixin needs.
    """

    _name = "school_enrollment_revenue_recognition_line"
    _description = "School Enrollment Revenue Recognition - Line"
    _inherit = [
        "mixin.account_move_double_line",
    ]
    _order = "enrollment_id, id"

    # Accounting Move Double Line Mixin (``mixin.account_move_double_line``)
    _move_id_field_name = "move_id"
    _currency_id_field_name = "currency_id"
    _debit_account_id_field_name = "debit_account_id"
    _credit_account_id_field_name = "credit_account_id"
    _debit_partner_id_field_name = "partner_id"
    _credit_partner_id_field_name = "partner_id"
    _debit_analytic_account_id_field_name = "analytic_account_id"
    _credit_analytic_account_id_field_name = "analytic_account_id"
    _debit_label_field_name = "name"
    _credit_label_field_name = "name"
    _debit_amount_currency_field_name = "amount"
    _credit_amount_currency_field_name = "amount"
    _debit_currency_id_field_name = "currency_id"
    _credit_currency_id_field_name = "currency_id"
    _debit_company_currency_id_field_name = "company_currency_id"
    _credit_company_currency_id_field_name = "company_currency_id"
    _debit_date_field_name = "date"
    _credit_date_field_name = "date"
    _debit_company_id_field_name = "company_id"
    _credit_company_id_field_name = "company_id"

    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        required=True,
        ondelete="cascade",
        help="The enrollment this Recognition Line belongs to.",
    )
    name = fields.Char(
        string="Label",
        required=True,
        help="Journal item label, copied from the originating detail line.",
    )
    payment_term_detail_id = fields.Many2one(
        string="Payment Term Detail",
        comodel_name="school_enrollment_payment_term_detail",
        ondelete="restrict",
        help="The invoiced payment term detail this Recognition Line releases.",
    )
    debit_account_id = fields.Many2one(
        string="Debit Account",
        comodel_name="account.account",
        help=(
            "Temporary account already used on the originating customer "
            "invoice line, debited by this Recognition Line."
        ),
    )
    credit_account_id = fields.Many2one(
        string="Credit Account",
        comodel_name="account.account",
        help=(
            "Final Account of the originating detail, credited by this "
            "Recognition Line."
        ),
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        help="Analytic Account copied from the originating customer invoice line.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        help="Partner copied from the originating customer invoice line.",
    )
    amount = fields.Monetary(
        string="Amount",
        currency_field="company_currency_id",
        help=(
            "Signed amount moved from the temporary account to the Final "
            "Account, copied from the originating customer invoice line's "
            "own subtotal."
        ),
    )
    move_id = fields.Many2one(
        string="Move",
        comodel_name="account.move",
        related="enrollment_id.recognition_move_id",
        help="Journal entry of the parent enrollment's Revenue Recognition.",
    )
    date = fields.Date(
        string="Date",
        related="enrollment_id.recognition_date",
        help="Accounting date inherited from the parent enrollment.",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="enrollment_id.company_id",
        help="Company inherited from the parent enrollment.",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        related="enrollment_id.company_currency_id",
        help="Company currency inherited from the parent enrollment.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="enrollment_id.currency_id",
        help="Currency inherited from the parent enrollment.",
    )
