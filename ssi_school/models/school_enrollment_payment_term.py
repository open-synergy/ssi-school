# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

ADDENDUM_LOCK_ALLOWED_FIELDS = {
    "customer_invoice_id",
    "manually_control",
    "locked",
    "sequence",
}


class SchoolEnrollmentPaymentTerm(models.Model):
    """
    Represents an actual payment billing term on a specific enrollment.
    SchoolEnrollmentPaymentTerm is a realized instance of a template term applied
    to a specific enrollment. Each term can generate one customer invoice
    (customer_invoice_id) via action_create_invoice. The state is automatically
    computed: draft (enrollment in draft/confirm), uninvoiced (enrollment
    open/done, no customer invoice yet), invoiced (customer invoice created),
    paid (the linked customer invoice is fully paid), manual (manually
    controlled), cancelled (enrollment cancelled).
    Totals (amount_untaxed, amount_tax, amount_total) are computed from detail_ids.
    """

    _name = "school_enrollment_payment_term"
    _description = "School Enrollment Payment Term"
    _order = "sequence, id"

    @api.depends(
        "customer_invoice_id",
        "customer_invoice_id.state",
        "enrollment_id.state",
        "manually_control",
        "detail_ids.voided",
    )
    def _compute_state(self):
        """Derive the billing state from the enrollment and invoice.

        ``draft`` while the enrollment is in ``draft`` or ``confirm``.
        Once the enrollment is ``open`` or ``done`` the value becomes
        ``paid`` when ``customer_invoice_id`` is set and that invoice's
        own ``state`` is ``done``, ``invoiced`` when it is set but not
        yet ``done``, ``voided`` when ``_is_fully_voided`` is true,
        ``manual`` when ``manually_control`` is enabled, and
        ``uninvoiced`` otherwise. Any other enrollment state
        (cancelled, rejected) yields ``cancelled``.

        :return: None
        """
        for record in self:
            if record.enrollment_id.state in ["draft", "confirm"]:
                state = "draft"
            elif record.enrollment_id.state in ["open", "done"]:
                if record.customer_invoice_id:
                    if record.customer_invoice_id.state == "done":
                        state = "paid"
                    else:
                        state = "invoiced"
                elif record._is_fully_voided():  # pylint: disable=protected-access
                    state = "voided"
                elif record.manually_control:
                    state = "manual"
                else:
                    state = "uninvoiced"
            else:
                state = "cancelled"
            record.state = state

    @api.depends(
        "detail_ids",
        "detail_ids.voided",
        "detail_ids.price_subtotal",
        "detail_ids.price_tax",
        "detail_ids.price_total",
    )
    def _compute_total(self):
        """Sum the detail lines into the payment term totals.

        ``amount_untaxed``, ``amount_tax``, and ``amount_total`` are
        the sums of ``price_subtotal``, ``price_tax``, and
        ``price_total`` over the detail lines that are not
        ``voided``; a term without invoiceable detail lines totals
        zero.

        :return: None
        """
        for record in self:
            amount_untaxed = amount_tax = amount_total = 0.0
            for detail in record.detail_ids:
                if detail.voided:
                    continue
                amount_untaxed += detail.price_subtotal
                amount_tax += detail.price_tax
                amount_total += detail.price_total
            record.amount_untaxed = amount_untaxed
            record.amount_tax = amount_tax
            record.amount_total = amount_total

    def _is_fully_voided(self):
        """Check whether this term has nothing left to invoice.

        Extension point: ``True`` when ``detail_ids`` is not empty
        and ``_get_invoiceable_detail`` returns nothing -- i.e. every
        detail line is ``voided``. A term without any detail line is
        never fully voided; it is simply empty. Modules that add
        another family of billing lines to this term (e.g. an
        extracurricular fee line) should override this single method
        instead of duplicating ``_compute_state`` or
        ``_create_invoice``.

        :return: bool
        """
        self.ensure_one()
        return bool(self.detail_ids) and not self._get_invoiceable_detail()

    def _get_invoiceable_detail(self):
        """Return the detail lines that still need to be invoiced.

        Extension point: filters out ``voided`` lines. Used by
        ``_create_invoice`` in place of ``self.detail_ids`` so a line
        whose amount has already moved to another term is never
        billed twice.

        :return: ``school_enrollment_payment_term_detail`` recordset
        """
        self.ensure_one()
        return self.detail_ids.filtered(lambda detail: not detail.voided)

    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        ondelete="cascade",
        help="The enrollment that owns this payment term.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="enrollment_id.student_id.contact_id",
        store=True,
        help=(
            "The student's contact partner, automatically "
            "populated from the enrollment."
        ),
    )
    name = fields.Char(
        string="Term",
        required=True,
        help=(
            "Name of the payment period, "
            "e.g. 'Registration Fee' or 'Monthly Tuition'."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help=(
            "Order of the payment period within the enrollment. "
            "Lower values appear first."
        ),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="enrollment_id.currency_id",
        store=True,
        required=False,
        help="The billing currency, automatically taken from the enrollment.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="enrollment_id.pricelist_id",
        store=True,
        help="The pricelist used, automatically taken from the enrollment.",
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="school_enrollment_payment_term_detail",
        inverse_name="term_id",
        copy=True,
        help="Product/fee detail lines within this payment period.",
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help=(
            "Total billing amount before tax, "
            "automatically computed from the detail lines."
        ),
    )
    amount_tax = fields.Monetary(
        string="Tax",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="Total tax amount, automatically computed from the detail lines.",
    )
    amount_total = fields.Monetary(
        string="Total",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help=(
            "Total billing amount including tax, "
            "automatically computed from the detail lines."
        ),
    )
    customer_invoice_id = fields.Many2one(
        string="# Customer Invoice",
        comodel_name="customer_invoice",
        readonly=True,
        ondelete="restrict",
        help="The customer invoice linked to this payment period.",
    )
    amount_unrealized = fields.Monetary(
        string="Unrealized",
        related="customer_invoice_id.amount_residual",
        store=True,
        currency_field="currency_id",
        readonly=True,
        help=(
            "Portion of this term still outstanding on the linked "
            "customer invoice. Zero when the term has no customer "
            "invoice yet."
        ),
    )
    date_invoice = fields.Date(
        string="Estimated Invoice Date",
        help="Estimated date for issuing the invoice for this billing period.",
    )
    date_due = fields.Date(
        string="Estimated Due Date",
        help="Estimated due date for payment of this billing period.",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("uninvoiced", "Uninvoiced"),
            ("invoiced", "Invoiced"),
            ("paid", "Paid"),
            ("voided", "Voided"),
            ("manual", "Manually Controlled"),
            ("cancelled", "Cancelled"),
        ],
        compute="_compute_state",
        store=True,
        help=(
            "Billing status: "
            "Draft = enrollment still in draft/confirm, "
            "Uninvoiced = enrollment open/done but no customer invoice yet, "
            "Invoiced = customer invoice created, "
            "Paid = the linked customer invoice is fully paid, "
            "Voided = every detail line has had its amount moved to "
            "another payment term, "
            "Manually Controlled = managed manually, "
            "Cancelled = enrollment cancelled."
        ),
    )
    manually_control = fields.Boolean(
        string="Manually Controlled",
        default=False,
        help=(
            "If enabled, this billing term is managed manually "
            "and does not require a customer invoice."
        ),
    )
    enrollment_state = fields.Selection(
        string="Enrollment State",
        related="enrollment_id.state",
        store=True,
        help=(
            "Status of the owning enrollment, used to control "
            "term-level actions such as duplication."
        ),
    )
    addendum_ok = fields.Boolean(
        string="Can Addendum",
        related="enrollment_id.addendum_ok",
        help=(
            "Whether the owning enrollment currently allows adding new "
            "payment terms/details via the addendum mechanism."
        ),
    )
    locked = fields.Boolean(
        string="Locked",
        default=False,
        readonly=True,
        copy=False,
        help=(
            "Automatically set to True when the enrollment is opened. "
            "Locked payment terms can no longer be edited or deleted; "
            "new terms added afterwards via the addendum mechanism start "
            "unlocked."
        ),
    )

    def _check_addendum_lock(self, vals):
        """Reject writes on a locked payment term.

        Guard called from ``write``. The write passes when the context
        carries ``bypass_addendum_lock``, or when every key of ``vals``
        belongs to ``ADDENDUM_LOCK_ALLOWED_FIELDS``
        (``customer_invoice_id``, ``manually_control``, ``locked``,
        ``sequence``) -- the bookkeeping fields that stay writable even
        after locking. Otherwise a locked term may not be changed and a
        new term has to be added through the addendum mechanism.

        :param vals: write values whose keys are checked against the
            allowed field set
        :raises UserError: when a locked term is written with a field
            outside the allowed set
        :return: None
        """
        if self.env.context.get("bypass_addendum_lock"):
            return
        if set(vals.keys()) <= ADDENDUM_LOCK_ALLOWED_FIELDS:
            return
        for record in self:
            if record.locked:
                error_message = (
                    _(
                        """
Context: Update payment term
Database ID: %s
Problem: Payment term '%s' is locked and cannot be modified
Solution: Add a new payment term via the addendum mechanism instead of editing this one
"""
                    )
                    % (record.id, record.name)
                )
                raise UserError(error_message)

    def _check_addendum_lock_unlink(self):
        """Reject deletion of a locked payment term.

        Guard called from ``unlink``. Deletion only passes when the
        context carries ``bypass_addendum_lock``; a locked term is
        permanent because it may already be reflected in a customer
        invoice, so a correction has to be booked as a new addendum
        term.

        :raises UserError: when a locked term is deleted
        :return: None
        """
        if self.env.context.get("bypass_addendum_lock"):
            return
        for record in self:
            if record.locked:
                error_message = (
                    _(
                        """
Context: Delete payment term
Database ID: %s
Problem: Payment term '%s' is locked and cannot be deleted
Solution: Locked payment terms are permanent; create a new one via addendum instead
"""
                    )
                    % (record.id, record.name)
                )
                raise UserError(error_message)

    def action_create_invoice(self):
        """Create the customer invoice of the selected payment terms.

        Triggered by the Create Invoice button on the payment term
        line. For every selected record, runs ``_create_invoice`` in
        ``sudo``, which creates one ``customer_invoice`` document with
        one line per detail and links it to the term. The term then
        shows as ``invoiced``.

        :return: None
        """
        for record in self.sudo():
            record._create_invoice()  # pylint: disable=protected-access

    def action_delete_invoice(self):
        """Delete the customer invoice of the selected payment terms.

        Triggered by the Delete Invoice button. For every selected
        record, runs ``_delete_invoice`` in ``sudo``, which detaches
        the detail lines and the term and then deletes the document --
        possible only while that document is still draft.

        :raises UserError: when the customer invoice is no longer draft
        :return: None
        """
        for record in self.sudo():
            record._delete_invoice()  # pylint: disable=protected-access

    def action_disconnect_invoice(self):
        """Detach the customer invoice from the selected terms.

        Triggered by the Disconnect Invoice button. For every selected
        record, runs ``_disconnect_invoice`` in ``sudo``, which clears
        ``customer_invoice_id`` so the term falls back to
        ``uninvoiced`` while the ``customer_invoice`` document itself
        is kept.

        :return: None
        """
        for record in self.sudo():
            record._disconnect_invoice()  # pylint: disable=protected-access

    def action_mark_as_manual(self):
        """Mark the selected payment terms as manually controlled.

        Triggered by the Mark as Manual button. For every selected
        record, runs ``_mark_as_manual`` in ``sudo``, which enables
        ``manually_control`` so the term is settled outside Odoo and
        shows as ``manual`` instead of ``uninvoiced``.

        :return: None
        """
        for record in self.sudo():
            record._mark_as_manual()  # pylint: disable=protected-access

    def action_unmark_as_manual(self):
        """Return the selected payment terms to invoice control.

        Triggered by the Unmark as Manual button. For every selected
        record, runs ``_unmark_as_manual`` in ``sudo``, which disables
        ``manually_control`` so the term shows as ``uninvoiced`` again
        and can be invoiced.

        :return: None
        """
        for record in self.sudo():
            record._unmark_as_manual()  # pylint: disable=protected-access

    def action_open_duplicate_wizard(self):
        """Open the duplicate wizard for this payment term.

        Triggered by the Duplicate button on the payment term line.
        Builds the wizard action through ``_open_duplicate_wizard`` in
        ``sudo``; when several records are selected only the action of
        the last one is returned.

        :return: dict window action of the duplicate wizard
        """
        for record in self.sudo():
            result = record._open_duplicate_wizard()
        return result

    def _open_duplicate_wizard(self):
        """Build the window action of the duplicate wizard.

        Reads the
        ``ssi_school.school_enrollment_payment_term_action_duplicate``
        action and injects a context whose ``active_id`` points at this
        term, so the wizard knows which term to copy.

        :return: dict window action of the duplicate wizard
        """
        self.ensure_one()
        waction = self.env.ref(
            "ssi_school.school_enrollment_payment_term_action_duplicate"
        ).read()[0]
        waction.update({"context": {"active_id": self.id}})
        return waction

    def _mark_as_manual(self):
        """Enable manual control on this payment term.

        Writes ``manually_control`` to ``True``, which moves the
        computed ``state`` to ``manual`` so the term is no longer
        expected to produce a customer invoice.

        :return: None
        """
        self.ensure_one()
        self.write({"manually_control": True})

    def _unmark_as_manual(self):
        """Disable manual control on this payment term.

        Writes ``manually_control`` to ``False``, which moves the
        computed ``state`` back to ``uninvoiced`` so the term is
        expected to produce a customer invoice again.

        :return: None
        """
        self.ensure_one()
        self.write({"manually_control": False})

    def _create_invoice(self):
        """Create the ``customer_invoice`` document for this term.

        Rejects a term that is fully voided -- the same predicate
        that drives ``state == "voided"``, so the two can never
        disagree. Otherwise creates the header first, then one
        ``customer_invoice.line`` per invoiceable detail line (see
        ``_get_invoiceable_detail``), writing the resulting line back
        onto the detail it originates from, and finally links the
        document to this term. Taxes are not computed here:
        ``customer_invoice`` recomputes them itself on pre-confirm.
        When the enrollment has ``auto_confirm_customer_invoice``
        enabled, the new document is confirmed right away.

        :raises UserError: when every detail line of this term is
            ``voided``
        :return: None
        """
        self.ensure_one()
        if self._is_fully_voided():  # pylint: disable=protected-access
            error_message = (
                _(
                    """
Context: Create customer invoice from payment term
Database ID: %s
Problem: Payment term '%s' has no invoiceable detail line -- every line was voided
Solution: Nothing to invoice; the amount was already billed on the term it moved to
"""
                )
                % (self.id, self.name)
            )
            raise UserError(error_message)
        line_model = self.env["customer_invoice.line"]
        invoice = self.env["customer_invoice"].create(self._prepare_invoice_data())
        for (
            detail
        ) in self._get_invoiceable_detail():  # pylint: disable=protected-access
            # pylint: disable=protected-access
            line_data = detail._prepare_invoice_line()
            line_data["customer_invoice_id"] = invoice.id
            line = line_model.create(line_data)
            detail.write({"customer_invoice_line_id": line.id})
        self.write({"customer_invoice_id": invoice.id})
        if self.enrollment_id.auto_confirm_customer_invoice:
            invoice.action_confirm()

    def _disconnect_invoice(self):
        """Detach the customer invoice from this term without deleting it.

        Only ``customer_invoice_id`` is cleared, so the term falls back to
        the uninvoiced state while the ``customer_invoice`` document itself
        is kept.

        :return: None
        """
        self.ensure_one()
        self.write({"customer_invoice_id": False})

    def _prepare_invoice_data(self):
        """Build the ``customer_invoice`` header values for this term.

        Extension point: override in a glue module (Operating Unit, for
        instance) to add extra header values without touching
        ``_create_invoice``. Detail lines are deliberately excluded --
        they are created one by one by ``_create_invoice`` so that each
        line can be written back to its originating detail.

        :return: dict of ``customer_invoice`` values
        """
        self.ensure_one()
        enrollment = self.enrollment_id
        date = self.date_invoice or fields.Date.today()
        return {
            "type_id": enrollment.customer_invoice_type_id.id,
            "partner_id": enrollment.student_id.contact_id.id,
            "currency_id": enrollment.currency_id.id,
            "pricelist_id": enrollment.pricelist_id.id,
            "journal_id": enrollment.receivable_journal_id.id,
            "receivable_account_id": enrollment.receivable_account_id.id,
            "date": date,
            "date_due": self.date_due or date,
            "customer_document_number": enrollment.name,
        }

    def _delete_invoice(self):
        """Delete the customer invoice document created from this term.

        Only a document still in ``draft`` may be deleted. Every detail
        line is unlinked from its ``customer_invoice.line`` first, then the
        term is detached, and finally the document is deleted (its lines
        are removed by cascade).

        :raises UserError: when the customer invoice is no longer draft
        :return: None
        """
        self.ensure_one()
        invoice = self.customer_invoice_id
        if invoice.state != "draft":
            error_message = (
                _(
                    """
Context: Delete customer invoice of payment term
Database ID: %s
Problem: Customer invoice '%s' is not draft anymore and cannot be deleted
Solution: Use Disconnect Invoice to detach it from the payment term instead
"""
                )
                % (self.id, invoice.display_name)
            )
            raise UserError(error_message)
        self.detail_ids.write({"customer_invoice_line_id": False})
        self.write({"customer_invoice_id": False})
        invoice.unlink()

    @api.model
    def create(self, vals):
        """Refresh the enrollment payment summary after creation.

        Overridden so that a term created outside the enrollment form
        -- by the payment template computation or the duplicate wizard
        -- still triggers ``_recompute_product_summaries`` on its
        enrollment, keeping ``product_summary_ids`` in step with the
        payment terms.

        :param vals: values of the payment term to create
        :return: created ``school_enrollment_payment_term`` record
        """
        result = super().create(vals)
        if result.enrollment_id:
            enrollment = result.enrollment_id
            enrollment._recompute_product_summaries()  # pylint: disable=protected-access
        return result

    def write(self, vals):
        """Enforce the addendum lock and refresh the payment summary.

        Overridden to run ``_check_addendum_lock`` before the write, so
        locked terms cannot be modified, and to recompute
        ``product_summary_ids`` on every touched enrollment afterwards.

        :param vals: values to write
        :raises UserError: when a locked term is written with a field
            outside ``ADDENDUM_LOCK_ALLOWED_FIELDS``
        :return: ``True``
        """
        self._check_addendum_lock(vals)
        result = super().write(vals)
        self.mapped(
            "enrollment_id"
        )._recompute_product_summaries()  # pylint: disable=protected-access
        return result

    def unlink(self):
        """Enforce the addendum lock and refresh the payment summary.

        Overridden to run ``_check_addendum_lock_unlink`` before the
        deletion, so locked terms cannot be removed, and to recompute
        ``product_summary_ids`` on the enrollments collected before the
        records disappear.

        :raises UserError: when a locked term is deleted
        :return: ``True``
        """
        self._check_addendum_lock_unlink()
        enrollments = self.mapped("enrollment_id")
        result = super().unlink()
        enrollments._recompute_product_summaries()  # pylint: disable=protected-access
        return result
