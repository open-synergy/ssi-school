# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolEnrollment(models.Model):
    """
    Represents the enrollment process of a student into a school for a specific
    academic term and grade. Enrollment is the primary transaction document
    recording a student's participation in one academic term. The approval
    workflow uses multi-approval mixins:
    Draft → Confirm → Approve → Open → Done / Cancel.
    After enrollment is completed (Done), the system records the academic result
    (academic_year_result) and the next promotion grade (promote_to_grade_id),
    which are used by SchoolStudent to update current_grade_id and next_grade_id.
    Enrollment also manages payment billing through payment_term_ids, and a
    payment template (payment_template_id) can be used to auto-populate billing.
    """

    _name = "school_enrollment"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "School Enrollment"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_done",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    date = fields.Date(
        string="Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The date the enrollment document was created.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The academic year this enrollment is based on.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The academic term in which the student is enrolled. "
            "Must belong to the selected academic year."
        ),
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The destination school for this enrollment.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        required=False,
        readonly=True,
        help=(
            "The education level type, automatically populated "
            "from the selected school."
        ),
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The class level the student will attend in this enrollment.",
    )
    grade_class_id = fields.Many2one(
        string="Grade Class",
        comodel_name="school_grade_class",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The specific homeroom class the student is placed in.",
    )
    homeroom_id = fields.Many2one(
        string="Homeroom",
        comodel_name="school_homeroom",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The Homeroom batch this enrollment was generated from or "
            "linked to, if any."
        ),
    )
    last_term = fields.Boolean(
        string="Last Term of Academic Year?",
        related="academic_term_id.last_term",
        store=True,
        compute_sudo=True,
        readonly=True,
        help=(
            "Indicates whether this is the last term of the academic year, "
            "derived from the term data."
        ),
    )
    allowed_student_ids = fields.Many2many(
        string="Allowed Students",
        comodel_name="school_student",
        compute="_compute_allowed_student_ids",
        store=False,
        compute_sudo=True,
        help=(
            "List of students eligible for selection in this enrollment, "
            "computed based on the selected grade and term."
        ),
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The student being enrolled.",
    )

    academic_year_result = fields.Selection(
        string="Academic Year Result",
        selection=[
            ("passed", "Passed"),
            ("failed", "Failed"),
            ("drop_out", "Drop Out"),
            ("graduate", "Graduate"),
        ],
        help=(
            "The student's academic result at the end of the enrollment period: "
            "Passed, Failed, Drop Out, or Graduate."
        ),
    )
    promote_to_grade_id = fields.Many2one(
        string="Promote To Grade",
        comodel_name="school_grade",
        help=(
            "The target grade for promotion if the student passes "
            "at the end of the academic year."
        ),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        default=lambda self: self.env.company.currency_id,
        help="The currency used for the enrollment payment billing.",
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelists",
        comodel_name="product.pricelist",
        compute="_compute_allowed_pricelist_ids",
        store=False,
        help="Available pricelists based on the selected currency.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The pricelist used to calculate enrollment billing amounts.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="student_id.contact_id",
        store=True,
        help=(
            "The student's contact partner, automatically "
            "populated from the student record."
        ),
    )
    payment_template_id = fields.Many2one(
        string="Payment Template",
        comodel_name="school_enrollment_payment_template",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "A payment template that can be applied to "
            "auto-populate the billing terms."
        ),
    )
    payment_term_ids = fields.One2many(
        string="Payment Terms",
        comodel_name="school_enrollment_payment_term",
        inverse_name="enrollment_id",
        help=(
            "The payment billing terms that must be settled "
            "by the student for this enrollment."
        ),
    )
    product_summary_ids = fields.One2many(
        string="Payment Summary",
        comodel_name="school_enrollment.product_summary",
        inverse_name="enrollment_id",
        help=(
            "Automatically maintained summary of all payment term details "
            "grouped by product. Recomputed on every change to payment terms "
            "or their detail lines."
        ),
    )
    receivable_journal_id = fields.Many2one(
        string="Receivable Journal",
        comodel_name="account.journal",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The accounting journal used to record receivables "
            "for this enrollment payment."
        ),
    )
    receivable_account_id = fields.Many2one(
        string="Receivable Account",
        comodel_name="account.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The receivable account used to record enrollment billing.",
    )
    customer_invoice_type_id = fields.Many2one(
        string="Customer Invoice Type",
        comodel_name="customer_invoice_type",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The customer invoice type used for every customer invoice "
            "generated from the payment terms of this enrollment."
        ),
    )
    auto_confirm_customer_invoice = fields.Boolean(
        string="Auto Confirm Customer Invoice",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "If enabled, the customer invoice created from a payment "
            "term of this enrollment is immediately confirmed instead "
            "of being left in draft."
        ),
    )
    pass_ok = fields.Boolean(
        string="Pass",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Pass action button is visible.",
    )
    fail_ok = fields.Boolean(
        string="Fail",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Fail action button is visible.",
    )
    drop_out_ok = fields.Boolean(
        string="Drop Out",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Drop Out action button is visible.",
    )
    graduate_ok = fields.Boolean(
        string="Graduate",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Graduate action button is visible.",
    )
    copy_payment_term_ok = fields.Boolean(
        string="Can Copy Payment Term",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether payment terms may be "
            "copied into this enrollment."
        ),
    )
    addendum_ok = fields.Boolean(
        string="Can Addendum",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether new payment terms/details may "
            "be added to this enrollment while it is On Progress (open), "
            "via the addendum mechanism. Existing terms/details created "
            "before the addendum remain locked."
        ),
    )
    create_invoice_ok = fields.Boolean(
        string="Can Create Due Invoice",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether invoices may be created for "
            "payment terms that are due, via the Create Due Invoice wizard."
        ),
    )
    amount_total = fields.Monetary(
        string="Total",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
        currency_field="currency_id",
        help=(
            "Total billing amount of the payment terms that are "
            "neither cancelled nor voided."
        ),
    )
    amount_paid = fields.Monetary(
        string="Paid",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
        currency_field="currency_id",
        help=(
            "Amount already realized on the invoiced payment terms "
            "that are neither cancelled nor voided."
        ),
    )
    amount_residual = fields.Monetary(
        string="Residual",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
        currency_field="currency_id",
        help=(
            "Outstanding amount still to be paid, i.e. the total "
            "amount minus the amount already paid."
        ),
    )
    payment_status = fields.Selection(
        string="Payment Status",
        selection=[
            ("no_payment", "No Payment"),
            ("unpaid", "Unpaid"),
            ("partial", "Partially Paid"),
            ("paid", "Paid"),
        ],
        compute="_compute_payment_status",
        store=True,
        compute_sudo=True,
        help=(
            "Payment status derived from the realized amounts of the "
            "payment terms that are neither cancelled nor voided."
        ),
    )

    def _recompute_product_summaries(self):
        """Rebuild ``product_summary_ids`` from the payment term lines.

        Aggregates ``uom_quantity``, ``price_subtotal``, ``price_tax``,
        and ``price_total`` of all ``payment_term_ids.detail_ids`` per
        product, deletes the existing summary records of the
        enrollment, and creates one
        ``school_enrollment.product_summary`` record per product.
        Detail lines without a product are skipped, and so are lines
        that are ``voided`` -- their amount is already counted again
        on the term it moved to. Runs in ``sudo`` and is called from
        ``create``, ``write``, and ``unlink`` of the payment term and
        payment term detail models.

        :return: None
        """
        for record in self.sudo():
            summary_data = {}
            for term in record.payment_term_ids:
                for detail in term.detail_ids:
                    if detail.voided:
                        continue
                    pid = detail.product_id.id
                    if not pid:
                        continue
                    if pid not in summary_data:
                        summary_data[pid] = {
                            "enrollment_id": record.id,
                            "product_id": pid,
                            "uom_quantity": 0.0,
                            "amount_untaxed": 0.0,
                            "amount_tax": 0.0,
                            "amount_total": 0.0,
                        }
                    summary_data[pid]["uom_quantity"] += detail.uom_quantity
                    summary_data[pid]["amount_untaxed"] += detail.price_subtotal
                    summary_data[pid]["amount_tax"] += detail.price_tax
                    summary_data[pid]["amount_total"] += detail.price_total
            record.product_summary_ids.unlink()
            Summary = self.env[
                "school_enrollment.product_summary"
            ]  # pylint: disable=invalid-name
            for data in summary_data.values():
                Summary.create(data)

    def _compute_policy(self):  # pylint: disable=missing-return
        """Delegate policy computation to the transaction mixins.

        Overridden only to give this model its own ``_compute_policy``
        entry point for the extra policy fields declared here
        (``pass_ok``, ``fail_ok``, ``drop_out_ok``, ``graduate_ok``,
        ``copy_payment_term_ok``, ``addendum_ok``,
        ``create_invoice_ok``); the values themselves are still
        produced by the mixin implementation reached through
        ``super()``.

        :return: None
        """
        _super = super()
        _super._compute_policy()  # pylint: disable=protected-access

    @api.depends(
        "payment_term_ids",
        "payment_term_ids.state",
        "payment_term_ids.amount_total",
        "payment_term_ids.amount_unrealized",
        "payment_term_ids.customer_invoice_id",
    )
    def _compute_amount(self):
        """Aggregate billing totals from the counted payment terms.

        A term counts toward the totals when its ``state`` is
        neither ``cancelled`` nor ``voided``. ``amount_total`` sums
        the ``amount_total`` of the counted terms; ``amount_paid``
        sums, for the counted terms that carry a
        ``customer_invoice_id``, ``amount_total`` minus
        ``amount_unrealized`` -- terms without an invoice contribute
        nothing; ``amount_residual`` is the difference between the
        two.

        :return: None
        """
        for record in self:
            amount_total = amount_paid = 0.0
            counted_terms = record.payment_term_ids.filtered(
                lambda term: term.state not in ("cancelled", "voided")
            )
            for term in counted_terms:
                amount_total += term.amount_total
                if term.customer_invoice_id:
                    amount_paid += term.amount_total - term.amount_unrealized
            record.amount_total = amount_total
            record.amount_paid = amount_paid
            record.amount_residual = amount_total - amount_paid

    @api.depends(
        "currency_id",
        "amount_total",
        "amount_paid",
    )
    def _compute_payment_status(self):
        """Derive the payment status from the aggregated amounts.

        Evaluated in order, stopping at the first match:
        ``no_payment`` when ``amount_total`` is zero or negative,
        ``paid`` when ``amount_paid`` covers ``amount_total``,
        ``unpaid`` when nothing has been paid yet, and ``partial``
        for everything else. Amounts are compared with
        ``currency_id.compare_amounts`` instead of raw float
        operators.

        :return: None
        """
        for record in self:
            compare = record.currency_id.compare_amounts
            if compare(record.amount_total, 0.0) <= 0:
                payment_status = "no_payment"
            elif compare(record.amount_paid, record.amount_total) >= 0:
                payment_status = "paid"
            elif compare(record.amount_paid, 0.0) <= 0:
                payment_status = "unpaid"
            else:
                payment_status = "partial"
            record.payment_status = payment_status

    @api.depends(
        "currency_id",
    )
    def _compute_allowed_pricelist_ids(self):
        """Compute the pricelists selectable on this enrollment.

        Fills ``allowed_pricelist_ids`` with every ``product.pricelist``
        whose ``currency_id`` equals the enrollment currency, so
        ``pricelist_id`` can only offer pricelists expressed in the
        same currency. Without a currency the field is left empty.

        :return: None
        """
        Pricelist = self.env["product.pricelist"]  # pylint: disable=invalid-name
        for record in self:
            result = []
            if record.currency_id:
                criteria = [("currency_id", "=", record.currency_id.id)]
                result = Pricelist.search(criteria).ids
            record.allowed_pricelist_ids = result

    @api.onchange(
        "currency_id",
    )
    def onchange_pricelist_id(self):
        self.pricelist_id = False

    @api.depends("academic_term_id", "grade_id", "school_id")
    def _compute_allowed_student_ids(self):
        """Determine which students may be selected for this enrollment.

        Two criteria are unioned: (1) regular eligibility, matching
        ``next_grade_id`` on the academic year's first term or
        ``current_grade_id`` on any other term; and (2) transfer-in
        eligibility, which admits any ``draft`` student flagged
        ``is_transfer_in`` in the same school, regardless of grade,
        so a student transferring in mid-year can be enrolled directly
        into the target grade of any term. The field stays empty until
        academic term, grade, and school are all set.

        :return: None
        """
        for record in self:
            result = False
            if record.academic_term_id and record.grade_id and record.school_id:
                criteria = [
                    ("state", "=", "draft"),
                    ("school_id", "=", record.school_id.id),
                ]
                if record.academic_term_id.first_term:
                    criteria += [("next_grade_id", "=", record.grade_id.id)]
                else:
                    criteria += [("current_grade_id", "=", record.grade_id.id)]
                student_ids = set(self.env["school_student"].search(criteria).ids)

                # Transfer-in students may be enrolled into any grade of any
                # term, regardless of their computed current/next grade.
                transfer_in_criteria = [
                    ("state", "=", "draft"),
                    ("school_id", "=", record.school_id.id),
                    ("is_transfer_in", "=", True),
                ]
                student_ids |= set(
                    self.env["school_student"].search(transfer_in_criteria).ids
                )

                result = list(student_ids)
            record.allowed_student_ids = result

    @api.onchange(
        "academic_year_id",
    )
    def onchange_academic_term_id(self):
        self.academic_term_id = False

    @api.onchange(
        "grade_type_id",
    )
    def onchange_grade_id(self):
        self.grade_id = False

    @api.onchange(
        "academic_term_id",
        "school_id",
        "grade_id",
    )
    def onchange_student_id(self):
        self.student_id = False

    @api.onchange(
        "grade_id",
        "school_id",
    )
    def onchange_grade_class_id(self):
        self.grade_class_id = False

    @api.onchange(
        "payment_template_id",
    )
    def onchange_receivable_journal_id(self):
        self.receivable_journal_id = False
        if self.payment_template_id:
            self.receivable_journal_id = self.payment_template_id.journal_id

    @api.onchange(
        "payment_template_id",
    )
    def onchange_receivable_account_id(self):
        self.receivable_account_id = False
        if self.payment_template_id:
            self.receivable_account_id = self.payment_template_id.receivable_account_id

    @api.onchange(
        "payment_template_id",
    )
    def onchange_customer_invoice_type_id(self):
        self.customer_invoice_type_id = False
        if self.payment_template_id:
            self.customer_invoice_type_id = (
                self.payment_template_id.customer_invoice_type_id
            )

    @api.onchange(
        "payment_template_id",
    )
    def onchange_auto_confirm_customer_invoice(self):
        self.auto_confirm_customer_invoice = False
        if self.payment_template_id:
            self.auto_confirm_customer_invoice = (
                self.payment_template_id.auto_confirm_customer_invoice
            )

    @api.constrains("academic_term_id", "academic_year_id")
    def _check_term_year_match(self):
        """Validate that the academic term belongs to the year.

        Rejects a record whose ``academic_term_id.year_id`` differs
        from its ``academic_year_id``; records where either field is
        still empty pass.

        :raises ValidationError: on academic term/year mismatch
        :return: None
        """
        for record in self:
            if (
                record.academic_term_id
                and record.academic_year_id
                and record.academic_term_id.year_id != record.academic_year_id
            ):
                error_message = (
                    _(
                        """
Context: Set enrollment academic term
Database ID: %s
Problem: Academic Term '%s' does not belong to Academic Year '%s'
Solution: Select an Academic Term that belongs to the selected Academic Year
"""
                    )
                    % (
                        record.id,
                        record.academic_term_id.name,
                        record.academic_year_id.name,
                    )
                )
                raise ValidationError(error_message)

    @api.constrains("grade_class_id", "grade_id", "school_id")
    def _check_grade_class_match(self):
        """Validate the grade class against the grade and school.

        Rejects a record whose ``grade_class_id`` belongs to a
        different ``grade_id`` or a different ``school_id`` than the
        enrollment itself. Records without a grade class are skipped.

        :raises ValidationError: on grade class mismatch
        :return: None
        """
        for record in self:
            if not record.grade_class_id:
                continue
            if (
                record.grade_class_id.grade_id != record.grade_id
                or record.grade_class_id.school_id != record.school_id
            ):
                error_message = (
                    _(
                        """
Context: Set enrollment grade class
Database ID: %s
Problem: Grade Class '%s' does not match the selected Grade/School
Solution: Select a Grade Class that belongs to the selected Grade and School
"""
                    )
                    % (record.id, record.grade_class_id.name)
                )
                raise ValidationError(error_message)

    @api.constrains("state")
    def _check_enrollment_window(self):
        """Validate that the term's enrollment window is open.

        Re-checked on every ``state`` change: an enrollment may only
        reach ``open`` while ``academic_term_id.enrollment_state`` is
        ``open``, so no student is enrolled outside the registration
        period of the academic term.

        :raises ValidationError: when the document reaches ``open``
            while the academic term is not open for enrollment
        :return: None
        """
        for record in self:
            if (
                record.state == "open"
                and record.academic_term_id.enrollment_state != "open"
            ):
                error_message = (
                    _(
                        """
Context: Open enrollment
Database ID: %s
Problem: Academic Term '%s' is not open for enrollment
Solution: Open the enrollment window on the academic term before opening this enrollment
"""
                    )
                    % (record.id, record.academic_term_id.name)
                )
                raise ValidationError(error_message)

    @api.constrains("state", "student_id", "academic_term_id")
    def _check_duplicate_active_enrollment(self):
        """Validate one active enrollment per student and term.

        Searches for another ``school_enrollment`` in state ``open``
        carrying the same ``student_id`` and ``academic_term_id``. Only
        records that are themselves ``open`` and have both fields set
        are checked, so drafts and cancelled documents may coexist.

        :raises ValidationError: when another open enrollment already
            exists for the same student and academic term
        :return: None
        """
        for record in self:
            if (
                record.state != "open"
                or not record.student_id
                or not record.academic_term_id
            ):
                continue
            duplicate = self.search(
                [
                    ("id", "!=", record.id),
                    ("student_id", "=", record.student_id.id),
                    ("academic_term_id", "=", record.academic_term_id.id),
                    ("state", "=", "open"),
                ]
            )
            if duplicate:
                error_message = (
                    _(
                        """
Context: Open enrollment
Database ID: %s
Problem: Student '%s' already has an active enrollment for term '%s'
Solution: Cancel or close the existing enrollment before opening a new one
"""
                    )
                    % (record.id, record.student_id.name, record.academic_term_id.name)
                )
                raise ValidationError(error_message)

    @api.constrains("state", "grade_class_id")
    def _check_grade_class_capacity(self):
        """Validate that the grade class capacity is not exceeded.

        Counts the enrollments already in state ``open`` for the same
        ``grade_class_id``, this one included, and rejects the record
        when that count exceeds ``grade_class_id.capacity``. Skipped
        while the record is not ``open`` or the class carries no
        capacity.

        :raises ValidationError: when the grade class is over capacity
        :return: None
        """
        for record in self:
            grade_class = record.grade_class_id
            if record.state != "open" or not grade_class or not grade_class.capacity:
                continue
            open_count = self.search_count(
                [
                    ("grade_class_id", "=", grade_class.id),
                    ("state", "=", "open"),
                ]
            )
            if open_count > grade_class.capacity:
                error_message = (
                    _(
                        """
Context: Open enrollment
Database ID: %s
Problem: Grade Class '%s' is at full capacity (%s/%s students)
Solution: Choose a different Grade Class or increase its capacity
"""
                    )
                    % (
                        record.id,
                        grade_class.name,
                        open_count,
                        grade_class.capacity,
                    )
                )
                raise ValidationError(error_message)

    def action_set_result_to_passed(self):
        """Close the enrollment with a Passed academic year result.

        Triggered by the Pass button. For every selected record, runs
        ``_set_result_to_passed`` in ``sudo``, which moves the document
        to Done, records the promotion grade, and returns the student
        to draft so the next enrollment can be made.

        :return: None
        """
        for record in self.sudo():
            record._set_result_to_passed()  # pylint: disable=protected-access

    def action_compute_payment(self):
        """Regenerate the payment terms from the payment template.

        Triggered by the Compute Payment button. For every selected
        record, runs ``_compute_payment_from_template`` in ``sudo``,
        which replaces the current ``payment_term_ids`` with terms and
        detail lines rebuilt from ``payment_template_id``.

        :return: None
        """
        for record in self.sudo():
            record._compute_payment_from_template()  # pylint: disable=protected-access

    def _compute_payment_from_template(self):
        """Rebuild the payment terms from ``payment_template_id``.

        Deletes every existing ``payment_term_ids`` record, then
        creates one ``school_enrollment_payment_term`` per template
        term (ordered by ``sequence``) and one
        ``school_enrollment_payment_term_detail`` per template detail,
        copying product, description, account, quantity, unit of
        measure, unit price, and taxes. ``date_invoice`` comes from the
        template term's ``date_invoice_duration_id`` applied to
        ``date``, and ``date_due`` from ``date_due_duration_id``
        applied to that invoice date, falling back to ``date``. Returns
        immediately when no template is set, leaving the existing terms
        untouched.

        :return: None
        """
        self.ensure_one()
        template = self.payment_template_id
        if not template:
            return
        self.payment_term_ids.unlink()
        Term = self.env[  # pylint: disable=invalid-name
            "school_enrollment_payment_term"
        ]
        Detail = self.env[  # pylint: disable=invalid-name
            "school_enrollment_payment_term_detail"
        ]
        for tterm in template.term_ids.sorted("sequence"):
            date_invoice = False
            date_due = False
            if tterm.date_invoice_duration_id:
                date_invoice = tterm.date_invoice_duration_id.get_duration(self.date)
            if tterm.date_due_duration_id:
                date_due = tterm.date_due_duration_id.get_duration(
                    date_invoice or self.date
                )
            term = Term.create(
                {
                    "enrollment_id": self.id,
                    "name": tterm.name,
                    "sequence": tterm.sequence,
                    "date_invoice": date_invoice,
                    "date_due": date_due,
                }
            )
            for tdetail in tterm.detail_ids.sorted("sequence"):
                Detail.create(
                    {
                        "term_id": term.id,
                        "product_id": tdetail.product_id.id,
                        "name": tdetail.name,
                        "account_id": tdetail.account_id.id,
                        "uom_quantity": tdetail.uom_quantity,
                        "uom_id": tdetail.uom_id.id if tdetail.uom_id else False,
                        "price_unit": tdetail.price_unit,
                        "tax_ids": [(6, 0, tdetail.tax_ids.ids)],
                    }
                )

    def action_set_result_to_failed(self):
        """Close the enrollment with a Failed academic year result.

        Triggered by the Fail button. For every selected record, runs
        ``_set_result_to_failed`` in ``sudo``, which moves the document
        to Done and returns the student to draft without recording a
        promotion grade, so the same grade can be enrolled again.

        :return: None
        """
        for record in self.sudo():
            record._set_result_to_failed()  # pylint: disable=protected-access

    def action_set_result_to_drop_out(self):
        """Close the enrollment with a Drop Out academic year result.

        Triggered by the Drop Out button on a single record. Runs
        ``_set_result_to_drop_out`` in ``sudo``, which moves the
        document to Done and sets the student to dropped.

        :return: None
        """
        self.ensure_one()
        for record in self.sudo():
            record._set_result_to_drop_out()  # pylint: disable=protected-access

    def action_set_result_to_graduate(self):
        """Close the enrollment with a Graduate academic year result.

        Triggered by the Graduate button on a single record. Runs
        ``_set_result_to_graduate`` in ``sudo``, which moves the
        document to Done and sets the student to graduated.

        :return: None
        """
        self.ensure_one()
        for record in self.sudo():
            record._set_result_to_graduate()  # pylint: disable=protected-access

    def _set_result_to_graduate(self):
        """Mark this enrollment Done and graduate the student.

        Calls ``action_done`` with ``bypass_policy_check`` so the
        transition is not blocked by the done policy, writes
        ``academic_year_result`` as ``graduate``, then calls
        ``action_set_to_graduate`` on ``student_id``.

        :return: None
        """
        self.ensure_one()
        self.with_context(bypass_policy_check=True).action_done()
        self.write(
            {
                "academic_year_result": "graduate",
            }
        )
        self.student_id.action_set_to_graduate()  # pylint: disable=no-member

    def _set_result_to_drop_out(self):
        """Mark this enrollment Done and drop the student out.

        Calls ``action_done`` with ``bypass_policy_check`` so the
        transition is not blocked by the done policy, writes
        ``academic_year_result`` as ``drop_out``, then calls
        ``action_set_to_dropped`` on ``student_id``.

        :return: None
        """
        self.ensure_one()
        self.with_context(bypass_policy_check=True).action_done()
        self.write(
            {
                "academic_year_result": "drop_out",
            }
        )
        self.student_id.action_set_to_dropped()  # pylint: disable=no-member

    def _set_result_to_failed(self):
        """Mark this enrollment Done with the student held back.

        Calls ``action_done`` with ``bypass_policy_check`` so the
        transition is not blocked by the done policy, writes
        ``academic_year_result`` as ``failed``, then returns
        ``student_id`` to draft so the same grade can be enrolled
        again. No ``promote_to_grade_id`` is recorded.

        :return: None
        """
        self.ensure_one()
        self.with_context(bypass_policy_check=True).action_done()
        self.write(
            {
                "academic_year_result": "failed",
            }
        )
        self.student_id.action_set_to_draft()  # pylint: disable=no-member

    def _set_result_to_passed(self):
        """Mark this enrollment Done and promote the student.

        Calls ``action_done`` with ``bypass_policy_check`` so the
        transition is not blocked by the done policy, writes
        ``academic_year_result`` as ``passed`` together with
        ``promote_to_grade_id`` taken from ``grade_id.next_grade_id``,
        then returns ``student_id`` to draft so the enrollment into
        that next grade can be made.

        :return: None
        """
        self.ensure_one()
        self.with_context(bypass_policy_check=True).action_done()
        next_grade_id = self.grade_id.next_grade_id.id  # pylint: disable=no-member
        self.write(
            {
                "academic_year_result": "passed",
                "promote_to_grade_id": next_grade_id,
            }
        )
        self.student_id.action_set_to_draft()  # pylint: disable=no-member

    @ssi_decorator.post_open_action()
    def _10_enroll_student(self):
        """Set the student to enrolled once the document is opened.

        Post-open hook: runs right after the enrollment reaches
        ``open`` and calls ``action_set_to_enroll`` on ``student_id``.

        :return: None
        """
        self.ensure_one()
        self.student_id.action_set_to_enroll()  # pylint: disable=no-member

    @ssi_decorator.post_open_action()
    def _20_lock_existing_payment_term(self):
        """Lock the existing payment terms when the document opens.

        Post-open hook: runs after ``_10_enroll_student`` once the
        enrollment reaches ``open`` and calls ``_lock_payment_term``,
        freezing the terms and detail lines that exist at that moment.
        Terms added later through the addendum mechanism stay unlocked
        until Close Addendum is used.

        :return: None
        """
        self.ensure_one()
        self._lock_payment_term()

    @ssi_decorator.post_done_action()
    def _30_unenroll_or_graduate_student(self):
        """Release the student once the enrollment is done.

        Post-done hook: runs after the enrollment reaches ``done`` and
        returns ``student_id`` to draft. The final student status for a
        passed, failed, dropped out, or graduated result is applied
        afterwards by the matching ``_set_result_to_*`` method, which
        is what called ``action_done`` in the first place.

        :return: None
        """
        self.ensure_one()
        self.student_id.action_set_to_draft()  # pylint: disable=no-member

    def action_close_addendum(self):
        """Close the addendum and lock the payment terms again.

        Triggered by the Close Addendum button. For every selected
        record, runs ``_lock_payment_term`` in ``sudo`` so the terms
        and detail lines added during the addendum become locked and
        can no longer be edited or deleted.

        :return: None
        """
        for record in self.sudo():
            record._lock_payment_term()  # pylint: disable=protected-access

    def action_open_create_due_invoice_wizard(self):
        """Open the Create Due Invoice wizard for this enrollment.

        Triggered by the Create Due Invoice button. Builds the wizard
        action through ``_open_create_due_invoice_wizard`` in ``sudo``;
        when several records are selected only the action of the last
        one is returned.

        :return: dict window action of the Create Due Invoice wizard
        """
        for record in self.sudo():
            # pylint: disable=protected-access
            result = record._open_create_due_invoice_wizard()
        return result

    def _open_create_due_invoice_wizard(self):
        """Build the window action of the Create Due Invoice wizard.

        Reads the
        ``ssi_school.school_enrollment_wizard_create_due_invoice_action``
        action and injects a context whose ``active_model``,
        ``active_id``, and ``active_ids`` point at this enrollment, so
        the wizard knows which document to invoice.

        :return: dict window action of the Create Due Invoice wizard
        """
        self.ensure_one()
        waction = self.env.ref(
            "ssi_school.school_enrollment_wizard_create_due_invoice_action"
        ).read()[0]
        waction.update(
            {
                "context": {
                    "active_model": "school_enrollment",
                    "active_id": self.id,
                    "active_ids": [self.id],
                },
            }
        )
        return waction

    def _create_due_invoice(self, date_start=False, date_end=False):
        """Invoice every payment term that is due in a date range.

        Enforces the create-invoice policy first, then calls
        ``_create_invoice`` on each payment term returned by
        ``_get_due_payment_term``. Every such call creates one
        ``customer_invoice`` document with its lines and links it to
        the term. Called by the Create Due Invoice wizard.

        :param date_start: optional lower bound on the term
            ``date_invoice``; falsy means no lower bound
        :param date_end: optional upper bound on the term
            ``date_invoice``; falsy means today
        :raises UserError: when ``create_invoice_ok`` is not satisfied
        :return: None
        """
        self.ensure_one()
        self._check_create_invoice_policy()
        for term in self._get_due_payment_term(date_start, date_end):
            term._create_invoice()  # pylint: disable=protected-access

    def _get_due_payment_term(self, date_start=False, date_end=False):
        """Return the payment terms that are due for invoicing.

        Filters ``payment_term_ids`` down to the terms still in state
        ``uninvoiced`` that carry a ``date_invoice`` inside the given
        range. Extension point: override to change which terms the
        Create Due Invoice wizard picks up.

        :param date_start: optional lower bound on ``date_invoice``;
            falsy means no lower bound
        :param date_end: optional upper bound on ``date_invoice``;
            falsy means today in the user's timezone
        :return: ``school_enrollment_payment_term`` recordset
        """
        self.ensure_one()
        date_end = date_end or fields.Date.context_today(self)
        return self.payment_term_ids.filtered(
            lambda r: r.state == "uninvoiced"
            and r.date_invoice
            and (not date_start or r.date_invoice >= date_start)
            and r.date_invoice <= date_end
        )

    def _check_create_invoice_policy(self):
        """Check the policy that guards due invoice creation.

        Passes immediately when ``bypass_policy_check`` is present in
        the context; otherwise the ``create_invoice_ok`` policy field
        must be satisfied before any invoice may be created.

        :raises UserError: when ``create_invoice_ok`` is not satisfied
        :return: ``True`` when the check is bypassed, otherwise None
        """
        self.ensure_one()
        if self.env.context.get("bypass_policy_check", False):
            return True
        if not self.create_invoice_ok:
            error_message = (
                _(
                    """
Context: Create due invoice
Database ID: %s
Problem: Document is not allowed to create due invoice
Solution: Check create due invoice policy prerequisite
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)

    def _lock_payment_term(self):
        """Lock every payment term and detail of this enrollment.

        Searches the ``school_enrollment_payment_term`` and
        ``school_enrollment_payment_term_detail`` records of this
        enrollment that are still unlocked and writes ``locked`` to
        ``True`` on them, passing ``bypass_addendum_lock`` in the
        context so the lock guards do not reject that very write.

        :return: None
        """
        self.ensure_one()
        Term = self.env[
            "school_enrollment_payment_term"
        ]  # pylint: disable=invalid-name
        Detail = self.env[  # pylint: disable=invalid-name
            "school_enrollment_payment_term_detail"
        ]
        terms = Term.search([("enrollment_id", "=", self.id), ("locked", "=", False)])
        if terms:
            terms.with_context(bypass_addendum_lock=True).write({"locked": True})
        details = Detail.search(
            [("term_id.enrollment_id", "=", self.id), ("locked", "=", False)]
        )
        if details:
            details.with_context(bypass_addendum_lock=True).write({"locked": True})

    def _unlock_payment_term(self):
        """Unlock every payment term and detail of this enrollment.

        Reverse of ``_lock_payment_term``: the locked
        ``school_enrollment_payment_term`` and
        ``school_enrollment_payment_term_detail`` records of this
        enrollment get ``locked`` written back to ``False``, passing
        ``bypass_addendum_lock`` in the context so the lock guards do
        not reject that very write.

        :return: None
        """
        self.ensure_one()
        Term = self.env[
            "school_enrollment_payment_term"
        ]  # pylint: disable=invalid-name
        Detail = self.env[  # pylint: disable=invalid-name
            "school_enrollment_payment_term_detail"
        ]
        terms = Term.search([("enrollment_id", "=", self.id), ("locked", "=", True)])
        if terms:
            terms.with_context(bypass_addendum_lock=True).write({"locked": False})
        details = Detail.search(
            [("term_id.enrollment_id", "=", self.id), ("locked", "=", True)]
        )
        if details:
            details.with_context(bypass_addendum_lock=True).write({"locked": False})

    @ssi_decorator.post_restart_action()
    def _10_unlock_payment_term(self):
        """Unlock the payment terms when the document is restarted.

        Post-restart hook: runs after the enrollment goes back to
        ``draft`` and calls ``_unlock_payment_term``, so the terms and
        detail lines become editable and deletable again.

        :return: None
        """
        self.ensure_one()
        self._unlock_payment_term()

    @ssi_decorator.pre_cancel_action()
    def _10_check_payment_term_invoice(self):
        """Block cancellation while a payment term is still invoiced.

        Pre-cancel hook: runs before the enrollment moves to ``cancel``
        and refuses the transition while any ``payment_term_ids``
        record still carries a ``customer_invoice_id``, so no invoice
        is left pointing at a cancelled enrollment.

        :raises UserError: when a payment term is still linked to a
            customer invoice
        :return: None
        """
        self.ensure_one()
        invoiced_terms = self.payment_term_ids.filtered(lambda r: r.customer_invoice_id)
        if invoiced_terms:
            error_message = (
                _(
                    """
Context: Cancel enrollment
Database ID: %s
Problem: Payment term '%s' is already linked to an invoice
Solution: Delete or disconnect the invoice on the payment term before cancelling this enrollment
"""
                )
                % (self.id, invoiced_terms[0].name)
            )
            raise UserError(error_message)

    @ssi_decorator.post_cancel_action()
    def _10_unenroll_student(self):
        """Return the student to draft on cancellation.

        Post-cancel hook: runs after the enrollment reaches ``cancel``
        and calls ``action_set_to_draft`` on ``student_id``, so the
        student is no longer counted as enrolled and can be enrolled
        again.

        :return: None
        """
        self.ensure_one()
        self.student_id.action_set_to_draft()  # pylint: disable=no-member

    @api.model
    def _get_policy_field(self):
        res = super(  # pylint: disable=super-with-arguments
            SchoolEnrollment, self
        )._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
            "pass_ok",
            "fail_ok",
            "drop_out_ok",
            "graduate_ok",
            "copy_payment_term_ok",
            "addendum_ok",
            "create_invoice_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
