# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class SchoolAdmissionFeeAnalysis(models.Model):
    """
    Read-only reporting model that flattens each admission payment term
    detail (fee) line together with its payment term and admission
    context (academic year/term, school, grade, student, product), for
    pivot-table registration fee analysis. Backed by a plain SQL view,
    not stored; always reflects current data.
    """

    _name = "school_admission_fee_analysis"
    _description = "School Admission Fee Analysis"
    _auto = False
    _order = "id desc"

    detail_id = fields.Many2one(
        string="Detail",
        comodel_name="school_admission_payment_term_detail",
        readonly=True,
        help="The payment term detail (fee line) this analysis row represents.",
    )
    term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_admission_payment_term",
        readonly=True,
        help="The payment term that owns the fee line.",
    )
    admission_id = fields.Many2one(
        string="Admission",
        comodel_name="school_admission",
        readonly=True,
        help="The admission that owns the payment term.",
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
        comodel_name="res.partner",
        readonly=True,
        help="The student's contact partner, taken from the admission.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        readonly=True,
        help="The destination school of the admission.",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        readonly=True,
        help="The company responsible for the admission.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        readonly=True,
        help="The academic year the admission is based on.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        readonly=True,
        help="The academic term the student is admitted into.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        readonly=True,
        help="The class level the student is admitted into.",
    )
    payment_template_id = fields.Many2one(
        string="Payment Template",
        comodel_name="school_admission_payment_template",
        readonly=True,
        help=(
            "The payment template used to auto-populate billing, if any. "
            "Also encodes the Internal/External admission track, since "
            "the template name carries that distinction."
        ),
    )
    customer_invoice_id = fields.Many2one(
        string="Customer Invoice",
        comodel_name="customer_invoice",
        readonly=True,
        help="The customer invoice linked to the payment term, if generated.",
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
            ("paid", "Paid"),
            ("voided", "Voided"),
            ("manual", "Manually Controlled"),
            ("cancelled", "Cancelled"),
        ],
        readonly=True,
        help=(
            "Billing status of the payment term: "
            "Draft = admission still in draft/confirm, "
            "Uninvoiced = admission open/done but no customer invoice yet, "
            "Invoiced = customer invoice created, "
            "Paid = the linked customer invoice is fully paid, "
            "Voided = every detail line has had its amount moved to "
            "another payment term, "
            "Manually Controlled = managed manually, "
            "Cancelled = the admission itself was cancelled."
        ),
    )
    admission_state = fields.Selection(
        string="Admission State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "On Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        readonly=True,
        help="Workflow state of the owning admission.",
    )
    admission_payment_status = fields.Selection(
        string="Admission Payment Status",
        selection=[
            ("no_payment", "No Payment"),
            ("unpaid", "Unpaid"),
            ("partial", "Partially Paid"),
            ("paid", "Paid"),
        ],
        readonly=True,
        help="Aggregate payment status of the owning admission.",
    )
    admission_date = fields.Date(
        string="Admission Date",
        readonly=True,
        help="Date the admission was made.",
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
        """Create the SQL view that backs this analysis model.

        Odoo calls this on every module install or update for an
        ``_auto = False`` model. The existing view is dropped first and
        recreated from ``_select_query``, so a changed query takes
        effect as soon as the module is updated.

        :return: None
        """
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE VIEW %s AS (%s)""" % (self._table, self._select_query())
        )

    def _select_query(self):
        """Return the SQL SELECT that feeds the analysis view.

        Joins ``school_admission_payment_term_detail`` to its payment
        term and its admission, and exposes the detail line id as the
        row ``id`` so one analysis row equals one fee line. Excludes
        ``voided`` detail lines -- their amount is already billed again
        as a line on the term it moved to, and keeping both would
        double-count the fee in the pivot. Extension point: override to
        add columns or joins; every added column must be matched by a
        field declared on this model.

        :return: str containing the SELECT statement
        """
        return """
            SELECT
                detail.id AS id,
                detail.id AS detail_id,
                detail.term_id AS term_id,
                term.admission_id AS admission_id,
                detail.product_id AS product_id,
                detail.product_category_id AS product_category_id,
                adm.student_id AS student_id,
                adm.school_id AS school_id,
                adm.company_id AS company_id,
                adm.academic_year_id AS academic_year_id,
                adm.academic_term_id AS academic_term_id,
                adm.grade_id AS grade_id,
                adm.payment_template_id AS payment_template_id,
                term.customer_invoice_id AS customer_invoice_id,
                term.name AS term_name,
                term.state AS term_state,
                adm.state AS admission_state,
                adm.payment_status AS admission_payment_status,
                adm.date AS admission_date,
                term.date_invoice AS date_invoice,
                term.date_due AS date_due,
                detail.currency_id AS currency_id,
                detail.uom_quantity AS uom_quantity,
                detail.price_unit AS price_unit,
                detail.price_subtotal AS price_subtotal,
                detail.price_tax AS price_tax,
                detail.price_total AS price_total
            FROM school_admission_payment_term_detail detail
            JOIN school_admission_payment_term term ON term.id = detail.term_id
            JOIN school_admission adm ON adm.id = term.admission_id
            WHERE detail.voided IS NOT TRUE
        """
