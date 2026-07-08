# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolAdmissionPaymentTemplate(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Master data template defining the payment schedule structure for
    school admission, used to populate payment terms on admission
    records for a specific school and grade.
    """

    _name = "school_admission_payment_template"
    _inherit = ["mixin.master_data"]
    _description = "School Admission Payment Template"

    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=False,
        help="The academic term this payment template applies to.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=False,
        help="The school this payment template applies to.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        store=True,
        help="The grade type derived from the selected school.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=False,
        help="The grade level for which this payment template applies.",
    )
    receivable_journal_id = fields.Many2one(
        string="Receivable Journal",
        comodel_name="account.journal",
        required=False,
        help=(
            "Default receivable journal copied into the admission "
            "when this template is selected."
        ),
    )
    receivable_account_id = fields.Many2one(
        string="Receivable Account",
        comodel_name="account.account",
        required=False,
        help=(
            "Default receivable account copied into the admission "
            "when this template is selected."
        ),
    )
    term_ids = fields.One2many(
        string="Payment Terms",
        comodel_name="school_admission_payment_template.term",
        inverse_name="template_id",
        copy=True,
        help=("The payment term items defining the schedule " "in this template."),
    )
    product_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Product Selection Method",
        required=True,
        help=(
            "How the allowed products for this template's fee lines "
            "are determined: a manual list, a search domain, or Python code."
        ),
    )
    product_ids = fields.Many2many(
        comodel_name="product.product",
        relation="rel_admission_payment_template_2_product",
        column1="template_id",
        column2="product_id",
        string="Products",
        help="Manually selected products allowed on this template's fee lines.",
    )
    product_domain = fields.Text(
        default="[]",
        string="Product Domain",
        help="Search domain used to determine allowed products.",
    )
    product_python_code = fields.Text(
        default="result = []",
        string="Product Python Code",
        help="Python code that sets `result` to the allowed product recordset.",
    )

    @api.onchange("school_id")
    def onchange_grade_id(self):
        self.grade_id = False
