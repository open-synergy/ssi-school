# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

ADDENDUM_LOCK_ALLOWED_FIELDS = {
    "customer_invoice_id",
    "manually_control",
    "locked",
    "sequence",
}


class SchoolAdmissionPaymentTerm(models.Model):
    """
    Represents a payment installment term within a school admission
    record, tracking customer invoice status, amounts, and due dates
    for one payment period. Each term can generate one customer invoice
    (customer_invoice_id) via action_create_invoice.
    """

    _name = "school_admission_payment_term"
    _description = "School Admission Payment Term"
    _order = "sequence, id"

    @api.depends(
        "customer_invoice_id",
        "admission_id.state",
        "manually_control",
        "detail_ids.voided",
    )
    def _compute_state(self):
        """Derive the term state from the admission and the invoice.

        ``draft`` while the admission is draft or confirm; once open or
        done the term is ``invoiced`` when a customer invoice exists,
        ``voided`` when ``_is_fully_voided`` is true, ``manual`` when
        it is manually controlled, otherwise ``uninvoiced``. Any other
        admission state yields ``cancelled``.
        """
        for record in self:
            if record.admission_id.state in ["draft", "confirm"]:
                state = "draft"
            elif record.admission_id.state in ["open", "done"]:
                if record.customer_invoice_id:
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
        """Sum the detail lines into the term amounts.

        ``amount_untaxed``, ``amount_tax`` and ``amount_total`` are the
        sums of ``price_subtotal``, ``price_tax`` and ``price_total`` of
        the detail lines that are not ``voided``; a term without
        invoiceable detail lines totals zero.
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
        another family of billing lines to this term should override
        this single method instead of duplicating ``_compute_state``
        or ``_create_invoice``.

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

        :return: ``school_admission_payment_term_detail`` recordset
        """
        self.ensure_one()
        return self.detail_ids.filtered(lambda detail: not detail.voided)

    admission_id = fields.Many2one(
        string="Admission",
        comodel_name="school_admission",
        ondelete="cascade",
        help=("The parent school admission record this payment " "term belongs to."),
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="admission_id.student_id",
        store=True,
        help="The student partner derived from the parent admission record.",
    )
    name = fields.Char(
        string="Term",
        required=True,
        help="The name or label for this payment installment term.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help=("Determines the display order of this term " "in the admission."),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="admission_id.currency_id",
        store=True,
        required=False,
        help="The currency derived from the parent admission record.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="admission_id.pricelist_id",
        store=True,
        help="The pricelist derived from the parent admission record.",
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="school_admission_payment_term_detail",
        inverse_name="term_id",
        copy=True,
        help="The individual fee items included in this payment term.",
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="The total amount before taxes for this term.",
    )
    amount_tax = fields.Monetary(
        string="Tax",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="The total tax amount for this term.",
    )
    amount_total = fields.Monetary(
        string="Total",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="The total amount including taxes for this term.",
    )
    amount_unrealized = fields.Monetary(
        string="Unrealized",
        related="customer_invoice_id.amount_residual",
        store=True,
        readonly=True,
        currency_field="currency_id",
        help=(
            "Portion of this term still outstanding on the linked "
            "customer invoice. Zero when the term has no customer "
            "invoice yet."
        ),
    )
    customer_invoice_id = fields.Many2one(
        string="# Customer Invoice",
        comodel_name="customer_invoice",
        readonly=True,
        ondelete="restrict",
        help="The customer invoice generated for this payment term, if any.",
    )
    date_invoice = fields.Date(
        string="Estimated Invoice Date",
        help="The estimated date when the invoice will be issued.",
    )
    date_due = fields.Date(
        string="Estimated Due Date",
        help="The estimated due date for payment of this term.",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("uninvoiced", "Uninvoiced"),
            ("invoiced", "Invoiced"),
            ("voided", "Voided"),
            ("manual", "Manually Controlled"),
            ("cancelled", "Cancelled"),
        ],
        compute="_compute_state",
        store=True,
        help=(
            "The current state of this payment term. Voided means "
            "every detail line has had its amount moved to another "
            "payment term."
        ),
    )
    manually_control = fields.Boolean(
        string="Manually Controlled",
        default=False,
        help=(
            "Marks this term as manually controlled, " "skipping automatic invoicing."
        ),
    )
    admission_state = fields.Selection(
        string="Admission State",
        related="admission_id.state",
        store=True,
        help=(
            "Status of the owning admission, used to control "
            "term-level actions such as duplication."
        ),
    )
    addendum_ok = fields.Boolean(
        string="Can Addendum",
        related="admission_id.addendum_ok",
        help=(
            "Whether the owning admission currently allows adding new "
            "payment terms/details via the addendum mechanism."
        ),
    )
    locked = fields.Boolean(
        string="Locked",
        default=False,
        readonly=True,
        copy=False,
        help=(
            "Automatically set to True when the admission is opened. "
            "Locked payment terms can no longer be edited or deleted; "
            "new terms added afterwards via the addendum mechanism start "
            "unlocked."
        ),
    )

    def _check_addendum_lock(self, vals):
        """Forbid editing a locked payment term.

        Skipped when the context flag ``bypass_addendum_lock`` is set,
        or when the write only touches the fields listed in
        ``ADDENDUM_LOCK_ALLOWED_FIELDS``.

        :param vals: the write values about to be applied
        :return: ``None``
        :raises UserError: when a locked term would be modified
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
        """Forbid deleting a locked payment term.

        Skipped when the context flag ``bypass_addendum_lock`` is set.

        :return: ``None``
        :raises UserError: when a locked term would be deleted
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

    @api.model
    def create(self, vals):
        """Create the term and refresh the admission product summary.

        Overridden so the aggregated ``product_summary_ids`` of the
        owning admission stays in sync with its payment terms.

        :param vals: values of the term to create
        :return: the created ``school_admission_payment_term`` record
        """
        result = super().create(vals)
        if result.admission_id:
            result.admission_id._recompute_product_summary()  # pylint: disable=protected-access
        return result

    def write(self, vals):
        """Write the term, enforcing the addendum lock first.

        Overridden both to reject edits on locked terms and to refresh
        the aggregated product summary of the owning admission.

        :param vals: values to write
        :return: ``True``
        :raises UserError: when a locked term would be modified
        """
        self._check_addendum_lock(vals)
        result = super().write(vals)
        self.mapped(
            "admission_id"
        )._recompute_product_summary()  # pylint: disable=protected-access
        return result

    def unlink(self):
        """Delete the term, enforcing the addendum lock first.

        Overridden both to reject deletion of locked terms and to
        refresh the aggregated product summary of the owning admission.

        :return: ``True``
        :raises UserError: when a locked term would be deleted
        """
        self._check_addendum_lock_unlink()
        admissions = self.mapped("admission_id")
        result = super().unlink()
        admissions._recompute_product_summary()  # pylint: disable=protected-access
        return result

    def action_create_invoice(self):
        """Create the customer invoice of this payment term.

        User-facing button; runs as superuser so the invoice can be
        created regardless of the acting user's accounting rights.

        :return: ``None``
        """
        for record in self.sudo():
            record._create_invoice()  # pylint: disable=protected-access

    def action_delete_invoice(self):
        """Delete the draft customer invoice of this payment term.

        User-facing button; runs as superuser.

        :return: ``None``
        :raises UserError: when the invoice is no longer draft
        """
        for record in self.sudo():
            record._delete_invoice()  # pylint: disable=protected-access

    def action_disconnect_invoice(self):
        """Detach the customer invoice without deleting it.

        User-facing button; runs as superuser. The term goes back to
        ``uninvoiced`` while the invoice document is kept.

        :return: ``None``
        """
        for record in self.sudo():
            record._disconnect_invoice()  # pylint: disable=protected-access

    def action_mark_as_manual(self):
        """Flag this term as manually controlled.

        User-facing button; the term then stays out of the automatic
        due-invoice creation.

        :return: ``None``
        """
        for record in self.sudo():
            record._mark_as_manual()  # pylint: disable=protected-access

    def action_unmark_as_manual(self):
        """Remove the manually controlled flag from this term.

        User-facing button; the term becomes eligible again for the
        automatic due-invoice creation.

        :return: ``None``
        """
        for record in self.sudo():
            record._unmark_as_manual()  # pylint: disable=protected-access

    def action_open_duplicate_wizard(self):
        """Open the wizard duplicating this payment term.

        :return: an ``ir.actions.act_window`` dict
        """
        for record in self.sudo():
            result = record._open_duplicate_wizard()
        return result

    def _open_duplicate_wizard(self):
        """Build the act_window opening the duplicate-term wizard.

        Reads the wizard action and injects this term as the active
        record so the wizard can prefill its defaults from it.

        :return: an ``ir.actions.act_window`` dict
        """
        self.ensure_one()
        waction = self.env.ref(
            "ssi_school_admission.school_admission_payment_term_action_duplicate"
        ).read()[0]
        waction.update({"context": {"active_id": self.id}})
        return waction

    def _mark_as_manual(self):
        """Set ``manually_control`` on this term.

        :return: ``None``
        """
        self.ensure_one()
        self.write({"manually_control": True})

    def _unmark_as_manual(self):
        """Clear ``manually_control`` on this term.

        :return: ``None``
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
        When the admission has ``auto_confirm_customer_invoice``
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
        if self.admission_id.auto_confirm_customer_invoice:
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
        admission = self.admission_id
        date = self.date_invoice or fields.Date.today()
        return {
            "type_id": admission.customer_invoice_type_id.id,
            "partner_id": admission.student_id.id,
            "currency_id": admission.currency_id.id,
            "pricelist_id": admission.pricelist_id.id,
            "journal_id": admission.receivable_journal_id.id,
            "receivable_account_id": admission.receivable_account_id.id,
            "date": date,
            "date_due": self.date_due or date,
            "customer_document_number": admission.name,
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
