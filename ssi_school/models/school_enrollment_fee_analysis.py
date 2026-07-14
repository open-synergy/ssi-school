# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class SchoolEnrollmentFeeAnalysis(models.Model):
    """
    Read-only reporting model that flattens each enrollment payment term
    detail (fee) line together with its payment term and enrollment
    context (academic year/term, school, grade, student, product), for
    pivot-table fee analysis. Backed by a plain SQL view, not stored;
    always reflects current data.
    """

    _name = "school_enrollment_fee_analysis"
    _description = "School Enrollment Fee Analysis"
    _auto = False
    _order = "id desc"

    detail_id = fields.Many2one(
        string="Detail",
        comodel_name="school_enrollment_payment_term_detail",
        readonly=True,
        help="The payment term detail (fee line) this analysis row represents.",
    )
    term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_enrollment_payment_term",
        readonly=True,
        help="The payment term that owns the fee line.",
    )
    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        readonly=True,
        help="The enrollment that owns the payment term.",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        readonly=True,
        help="The product/fee type billed on this line.",
    )
    product_category_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        readonly=True,
        help="The category of the billed product.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        readonly=True,
        help="The student being billed, taken from the enrollment.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        readonly=True,
        help="The student's contact partner, taken from the enrollment.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        readonly=True,
        help="The destination school of the enrollment.",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        readonly=True,
        help="The company that owns the school of the enrollment.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        readonly=True,
        help="The academic year the enrollment is based on.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        readonly=True,
        help="The academic term the student is enrolled in.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        readonly=True,
        help="The class level the student attends in this enrollment.",
    )
    grade_class_id = fields.Many2one(
        string="Grade Class",
        comodel_name="school_grade_class",
        readonly=True,
        help="The specific homeroom class the student is placed in.",
    )
    payment_template_id = fields.Many2one(
        string="Payment Template",
        comodel_name="school_enrollment_payment_template",
        readonly=True,
        help="The payment template used to auto-populate billing, if any.",
    )
    invoice_id = fields.Many2one(
        string="Invoice",
        comodel_name="account.move",
        readonly=True,
        help="The invoice linked to the payment term, if already generated.",
    )
    term_name = fields.Char(
        string="Term",
        readonly=True,
        help="Name of the billing period, e.g. 'Registration Fee'.",
    )
    term_state = fields.Selection(
        string="Term State",
        selection=[
            ("draft", "Draft"),
            ("uninvoiced", "Uninvoiced"),
            ("invoiced", "Invoiced"),
            ("manual", "Manually Controlled"),
            ("cancelled", "Cancelled"),
        ],
        readonly=True,
        help=(
            "Billing status of the payment term: "
            "Draft = enrollment still in draft/confirm, "
            "Uninvoiced = enrollment open/done but no invoice yet, "
            "Invoiced = invoice created, "
            "Manually Controlled = managed manually, "
            "Cancelled = enrollment cancelled."
        ),
    )
    enrollment_state = fields.Selection(
        string="Enrollment State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "On Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        readonly=True,
        help="Workflow state of the owning enrollment.",
    )
    academic_year_result = fields.Selection(
        string="Academic Year Result",
        selection=[
            ("passed", "Passed"),
            ("failed", "Failed"),
            ("drop_out", "Drop Out"),
            ("graduate", "Graduate"),
        ],
        readonly=True,
        help="The student's academic result at the end of the enrollment period.",
    )
    enrollment_date = fields.Date(
        string="Enrollment Date",
        readonly=True,
        help="Date the enrollment was made.",
    )
    date_invoice = fields.Date(
        string="Estimated Invoice Date",
        readonly=True,
        help="Estimated date for issuing the invoice for this billing period.",
    )
    date_due = fields.Date(
        string="Estimated Due Date",
        readonly=True,
        help="Estimated due date for payment of this billing period.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        readonly=True,
        help="The billing currency of the fee line.",
    )
    uom_quantity = fields.Float(
        string="Qty",
        readonly=True,
        help="Quantity billed on the fee line.",
    )
    price_unit = fields.Monetary(
        string="Unit Price",
        currency_field="currency_id",
        readonly=True,
        help="Unit price of the fee line.",
    )
    price_subtotal = fields.Monetary(
        string="Untaxed",
        currency_field="currency_id",
        readonly=True,
        help="Untaxed subtotal of the fee line.",
    )
    price_tax = fields.Monetary(
        string="Tax",
        currency_field="currency_id",
        readonly=True,
        help="Tax amount of the fee line.",
    )
    price_total = fields.Monetary(
        string="Total",
        currency_field="currency_id",
        readonly=True,
        help="Total amount (including tax) of the fee line.",
    )

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE VIEW %s AS (%s)""" % (self._table, self._select_query())
        )

    def _select_query(self):
        return """
            SELECT
                detail.id AS id,
                detail.id AS detail_id,
                detail.term_id AS term_id,
                term.enrollment_id AS enrollment_id,
                detail.product_id AS product_id,
                detail.product_category_id AS product_category_id,
                enr.student_id AS student_id,
                enr.partner_id AS partner_id,
                enr.school_id AS school_id,
                sch.company_id AS company_id,
                enr.academic_year_id AS academic_year_id,
                enr.academic_term_id AS academic_term_id,
                enr.grade_id AS grade_id,
                enr.grade_class_id AS grade_class_id,
                enr.payment_template_id AS payment_template_id,
                term.invoice_id AS invoice_id,
                term.name AS term_name,
                term.state AS term_state,
                enr.state AS enrollment_state,
                enr.academic_year_result AS academic_year_result,
                enr.date AS enrollment_date,
                term.date_invoice AS date_invoice,
                term.date_due AS date_due,
                detail.currency_id AS currency_id,
                detail.uom_quantity AS uom_quantity,
                detail.price_unit AS price_unit,
                detail.price_subtotal AS price_subtotal,
                detail.price_tax AS price_tax,
                detail.price_total AS price_total
            FROM school_enrollment_payment_term_detail detail
            JOIN school_enrollment_payment_term term ON term.id = detail.term_id
            JOIN school_enrollment enr ON enr.id = term.enrollment_id
            LEFT JOIN school sch ON sch.id = enr.school_id
        """
