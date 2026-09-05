# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolAdmission(models.Model):
    """
    Represents the final school admission record for a student,
    tracking the admission decision, payment setup, and the creation
    of the student's enrollment profile after approval.
    """

    _name = "school_admission"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "School Admission"

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
        "create_enrollment_ok",
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
        help="The date of this admission.",
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
        help=("The academic year for which the student " "is being admitted."),
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
        help="The academic term associated with this admission.",
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
        help="The school the student is being admitted to.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="school_id.grade_type_id",
        required=False,
        readonly=True,
        help="The grade type derived from the selected school.",
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
        help="The grade level the student is being admitted to.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The student being admitted to the school.",
    )
    admission_form_id = fields.Many2one(
        string="Admission Form",
        comodel_name="school_admission_form",
        readonly=True,
        help="The admission form that initiated this admission, if any.",
    )
    admission_test_id = fields.Many2one(
        string="Admission Test",
        comodel_name="school_admission_test",
        readonly=True,
        help=("The admission test associated with this admission, " "if any."),
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
        help=("The currency used for payment calculations " "in this admission."),
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelists",
        comodel_name="product.pricelist",
        compute="_compute_allowed_pricelist_ids",
        store=False,
        help="Pricelists available based on the selected currency.",
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
        help=("The pricelist applied for price calculations " "in this admission."),
    )
    payment_template_id = fields.Many2one(
        string="Payment Template",
        comodel_name="school_admission_payment_template",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The payment template used to generate payment " "terms for this admission."
        ),
    )
    payment_term_ids = fields.One2many(
        string="Payment Terms",
        comodel_name="school_admission_payment_term",
        inverse_name="admission_id",
        help="The payment installment terms defined for this admission.",
    )
    product_summary_ids = fields.One2many(
        string="Product Summary",
        comodel_name="school_admission_product_summary",
        inverse_name="admission_id",
        help="Aggregated payment amounts per product across all payment terms.",
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
        help=("The journal used to post receivable entries " "for admission payments."),
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
        help=("The account used to record receivables " "for admission payments."),
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
            "generated from the payment terms of this admission."
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
            "term of this admission is immediately confirmed instead "
            "of being left in draft."
        ),
    )
    school_student_id = fields.Many2one(
        string="School Student",
        comodel_name="school_student",
        readonly=True,
        help=("The student profile created when this " "admission is opened."),
    )
    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        readonly=True,
        help=(
            "The school enrollment created from this admission via the "
            "Create Enrollment wizard, if any."
        ),
    )
    copy_payment_term_ok = fields.Boolean(
        string="Can Copy Payment Term",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether payment terms may be "
            "copied into this admission."
        ),
    )
    addendum_ok = fields.Boolean(
        string="Can Addendum",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether new payment terms/details may "
            "be added to this admission while it is On Progress (open), "
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
    create_enrollment_ok = fields.Boolean(
        string="Can Create Enrollment",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether the Create Enrollment button "
            "is visible, allowing a school_enrollment to be generated "
            "from this admission."
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

    def _compute_policy(self):  # pylint: disable=missing-return
        """Recompute every ``*_ok`` policy field of this admission.

        Delegates to the mixin implementation; it is redefined here only
        so the extra policy fields declared by this model (
        ``copy_payment_term_ok``, ``addendum_ok``, ``create_invoice_ok``,
        ``create_enrollment_ok``) are evaluated together with the
        standard workflow policies.
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
        """List the pricelists usable with the selected currency.

        Searches ``product.pricelist`` for records whose currency equals
        ``currency_id``; the result feeds the domain of ``pricelist_id``.
        Empty when no currency is set yet.
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
        "payment_template_id",
    )
    def onchange_receivable_journal_id(self):
        self.receivable_journal_id = False
        if self.payment_template_id:
            self.receivable_journal_id = self.payment_template_id.receivable_journal_id

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

    def action_compute_payment(self):
        """Regenerate the payment terms from the payment template.

        User-facing button. Runs as superuser so the terms and their
        details can be replaced regardless of the acting user's rights
        on those models.

        :return: ``None``
        """
        for record in self.sudo():
            record._compute_payment_from_template()  # pylint: disable=protected-access

    def _compute_payment_from_template(self):
        """Rebuild ``payment_term_ids`` from ``payment_template_id``.

        Deletes every existing payment term of this admission, then
        recreates one ``school_admission_payment_term`` per template
        term and one ``school_admission_payment_term_detail`` per
        template detail. Invoice and due dates are derived from the
        template duration records, relative to ``date``. Finally
        refreshes the product summary lines.

        Does nothing when no payment template is set.

        :return: ``None``
        """
        self.ensure_one()
        template = self.payment_template_id
        if not template:
            return
        self.payment_term_ids.unlink()
        Term = self.env["school_admission_payment_term"]  # pylint: disable=invalid-name
        Detail = self.env[
            "school_admission_payment_term_detail"
        ]  # pylint: disable=invalid-name
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
                    "admission_id": self.id,
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
        self._recompute_product_summary()

    def _recompute_product_summary(self):
        """Rebuild ``product_summary_ids`` from the payment terms.

        Drops the existing summary lines, then aggregates the subtotal,
        tax and total of every payment term detail per product and
        creates one summary line per product. Detail lines that are
        ``voided`` are skipped -- their amount is already counted
        again on the term it moved to.

        :return: ``None``
        """
        for record in self:
            record.product_summary_ids.unlink()
            product_data = {}
            for term in record.payment_term_ids:
                for detail in term.detail_ids:
                    if detail.voided:
                        continue
                    pid = detail.product_id.id
                    if not pid:
                        continue
                    if pid not in product_data:
                        product_data[pid] = {
                            "product_id": pid,
                            "amount_untaxed": 0.0,
                            "amount_tax": 0.0,
                            "amount_total": 0.0,
                        }
                    product_data[pid]["amount_untaxed"] += detail.price_subtotal
                    product_data[pid]["amount_tax"] += detail.price_tax
                    product_data[pid]["amount_total"] += detail.price_total
            Summary = self.env[
                "school_admission_product_summary"
            ]  # pylint: disable=invalid-name
            for seq, data in enumerate(product_data.values(), start=1):
                Summary.create(
                    {
                        "admission_id": record.id,
                        "sequence": seq * 5,
                        **data,
                    }
                )

    @ssi_decorator.post_open_action()
    def _20_lock_existing_payment_term(self):
        """Lock every payment term once the admission is opened.

        ``ssi_decorator`` hook executed after the transition to the
        ``open`` state, so terms agreed upon at admission time can no
        longer be edited except through the addendum mechanism.

        :return: ``None``
        """
        self.ensure_one()
        self._lock_payment_term()

    def action_close_addendum(self):
        """Close the addendum period by locking all payment terms.

        User-facing button available while the admission is on progress.
        Every payment term and term detail that is still unlocked is
        locked, so further changes require a new addendum.

        :return: ``None``
        """
        for record in self.sudo():
            record._lock_payment_term()  # pylint: disable=protected-access

    def action_open_create_due_invoice_wizard(self):
        """Open the Create Due Invoice wizard for this admission.

        :return: an ``ir.actions.act_window`` dict
        """
        for record in self.sudo():
            # pylint: disable=protected-access
            result = record._open_create_due_invoice_wizard()
        return result

    def _open_create_due_invoice_wizard(self):
        """Build the act_window opening the Create Due Invoice wizard.

        Reads the wizard action and injects this admission as the active
        record so the wizard can read its due payment terms.

        :return: an ``ir.actions.act_window`` dict
        """
        self.ensure_one()
        waction = self.env.ref(
            "ssi_school_admission.school_admission_wizard_create_due_invoice_action"
        ).read()[0]
        waction.update(
            {
                "context": {
                    "active_model": "school_admission",
                    "active_id": self.id,
                    "active_ids": [self.id],
                },
            }
        )
        return waction

    def action_create_enrollment(self):
        """Open the Create Enrollment wizard, or the linked enrollment.

        For each record: if ``enrollment_id`` is already set, return an
        act_window opening that enrollment's form directly. Otherwise,
        return an act_window opening the
        ``school_admission.wizard_create_enrollment`` wizard (in a new
        dialog) with ``admission_id`` and the currency/pricelist/journal/
        account defaults pre-filled from this admission.

        :return: an ``ir.actions.act_window`` dict
        """
        for record in self.sudo():
            result = record._open_create_enrollment_wizard()
        return result

    def _open_create_enrollment_wizard(self):
        """Build the act_window that opens the enrollment or its wizard.

        :return: an ``ir.actions.act_window`` dict
        """
        self.ensure_one()
        if self.enrollment_id:
            return {
                "type": "ir.actions.act_window",
                "name": "School Enrollment",
                "res_model": "school_enrollment",
                "res_id": self.enrollment_id.id,
                "view_mode": "form",
                "target": "current",
            }
        waction = self.env.ref(
            "ssi_school_admission.school_admission_wizard_create_enrollment_action"
        ).read()[0]
        waction.update(
            {
                "context": {
                    "default_admission_id": self.id,
                    "default_currency_id": self.currency_id.id,
                    "default_pricelist_id": self.pricelist_id.id,
                    "default_receivable_journal_id": self.receivable_journal_id.id,
                    "default_receivable_account_id": self.receivable_account_id.id,
                },
            }
        )
        return waction

    def _create_due_invoice(self, date_start=False, date_end=False):
        """Create a customer invoice for every due payment term.

        Checks the create-invoice policy first, then invoices each
        uninvoiced payment term whose invoice date falls in the given
        range.

        :param date_start: lower bound of ``date_invoice``, or ``False``
        :param date_end: upper bound of ``date_invoice``; defaults to
            today when omitted
        :return: ``None``
        :raises UserError: when ``create_invoice_ok`` is not satisfied
        """
        self.ensure_one()
        self._check_create_invoice_policy()
        for term in self._get_due_payment_term(date_start, date_end):
            term._create_invoice()  # pylint: disable=protected-access

    def _get_due_payment_term(self, date_start=False, date_end=False):
        """Select the payment terms that are due for invoicing.

        Extension point: override to change which terms are considered
        due without touching ``_create_due_invoice``.

        :param date_start: lower bound of ``date_invoice``, or ``False``
        :param date_end: upper bound of ``date_invoice``; defaults to
            today when omitted
        :return: a ``school_admission_payment_term`` recordset in state
            ``uninvoiced``
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
        """Verify this admission may create invoices for due terms.

        Skipped when the context flag ``bypass_policy_check`` is set.

        :return: ``True`` when the check is bypassed
        :raises UserError: when ``create_invoice_ok`` is ``False``
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
        """Lock every unlocked payment term and term detail.

        Writes ``locked = True`` with ``bypass_addendum_lock`` in the
        context, because the addendum constraint itself forbids writing
        on locked records.

        :return: ``None``
        """
        self.ensure_one()
        Term = self.env["school_admission_payment_term"]  # pylint: disable=invalid-name
        Detail = self.env[  # pylint: disable=invalid-name
            "school_admission_payment_term_detail"
        ]
        terms = Term.search([("admission_id", "=", self.id), ("locked", "=", False)])
        if terms:
            terms.with_context(bypass_addendum_lock=True).write({"locked": True})
        details = Detail.search(
            [("term_id.admission_id", "=", self.id), ("locked", "=", False)]
        )
        if details:
            details.with_context(bypass_addendum_lock=True).write({"locked": True})

    def _unlock_payment_term(self):
        """Unlock every locked payment term and term detail.

        Counterpart of ``_lock_payment_term``, used when the admission
        goes back to draft so its payment plan becomes editable again.

        :return: ``None``
        """
        self.ensure_one()
        Term = self.env["school_admission_payment_term"]  # pylint: disable=invalid-name
        Detail = self.env[  # pylint: disable=invalid-name
            "school_admission_payment_term_detail"
        ]
        terms = Term.search([("admission_id", "=", self.id), ("locked", "=", True)])
        if terms:
            terms.with_context(bypass_addendum_lock=True).write({"locked": False})
        details = Detail.search(
            [("term_id.admission_id", "=", self.id), ("locked", "=", True)]
        )
        if details:
            details.with_context(bypass_addendum_lock=True).write({"locked": False})

    @ssi_decorator.post_restart_action()
    def _10_unlock_payment_term(self):
        """Unlock all payment terms when the admission is restarted.

        ``ssi_decorator`` hook executed after the transition back to
        ``draft``.

        :return: ``None``
        """
        self.ensure_one()
        self._unlock_payment_term()

    @ssi_decorator.pre_cancel_action()
    def _10_check_payment_term_invoice(self):
        """Forbid cancelling while a payment term is invoiced.

        ``ssi_decorator`` hook executed before the transition to the
        ``cancel`` state.

        :return: ``None``
        :raises UserError: when at least one payment term still links to
            a customer invoice
        """
        self.ensure_one()
        invoiced_terms = self.payment_term_ids.filtered(lambda r: r.customer_invoice_id)
        if invoiced_terms:
            error_message = (
                _(
                    """
Context: Cancel admission
Database ID: %s
Problem: Payment term '%s' is already linked to an invoice
Solution: Delete or disconnect the invoice on the payment term before cancelling this admission
"""
                )
                % (self.id, invoiced_terms[0].name)
            )
            raise UserError(error_message)

    @ssi_decorator.post_open_action()
    def _10_create_school_student(self):
        """Create the student profile when the admission is opened.

        ``ssi_decorator`` hook executed after the transition to the
        ``open`` state. Creates one ``school_student`` from the admitted
        contact and stores it in ``school_student_id``. Does nothing
        when the profile already exists.

        :return: ``None``
        """
        self.ensure_one()
        if self.school_student_id:
            return
        initial_grade = (
            self.grade_id.previous_grade_id or False
        )  # pylint: disable=no-member
        student = self.env["school_student"].create(
            {
                "code": "/",
                "contact_id": self.student_id.id,
                "name": self.student_id.name,
                "school_id": self.school_id.id,
                "initial_grade_id": initial_grade.id if initial_grade else False,
            }
        )
        self.write({"school_student_id": student.id})

    @api.model
    def _get_policy_field(self):
        res = super(
            SchoolAdmission, self
        )._get_policy_field()  # pylint: disable=super-with-arguments
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
            "copy_payment_term_ok",
            "addendum_ok",
            "create_invoice_ok",
            "create_enrollment_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
