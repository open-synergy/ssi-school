# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SchoolAdmissionWizardCreateDueInvoice(models.TransientModel):
    """
    Wizard that creates invoices for all uninvoiced payment terms whose
    estimated invoice date (date_invoice) falls within a given date range, for
    one or more admissions selected from the school_admission list view or
    from a single admission's form. Every selected admission must be allowed
    by the create_invoice_ok policy (state and group, configurable via Policy
    Template). All admissions are validated before any invoice is created.
    """

    _name = "school_admission.wizard_create_due_invoice"
    _description = "Create Due Invoice for Admission Payment Terms"

    admission_ids = fields.Many2many(
        string="Admissions",
        comodel_name="school_admission",
        relation="rel_school_admission_create_due_invoice",
        column1="wizard_id",
        column2="admission_id",
        readonly=True,
        help="Admissions whose due payment terms will be invoiced.",
    )
    date_start = fields.Date(
        string="Date Start",
        help=(
            "Earliest estimated invoice date to process. "
            "Leave empty for no lower bound."
        ),
    )
    date_end = fields.Date(
        string="Date End",
        help=(
            "Latest estimated invoice date to process. "
            "Leave empty to process up to today."
        ),
    )

    @api.model
    def default_get(self, fields_list):
        """Prefill the admissions from the list view or form selection.

        :param fields_list: names of the fields to default
        :return: dict of default values
        """
        res = super().default_get(fields_list)
        if self.env.context.get("active_model") == "school_admission":
            active_ids = self.env.context.get("active_ids", [])
            res["admission_ids"] = [(6, 0, active_ids)]
        return res

    def action_create_due_invoice(self):
        """Invoice the due payment terms of the selected admissions.

        User-facing wizard button; runs as superuser so invoices may be
        created regardless of the acting user's accounting rights.

        :return: an ``ir.actions.act_window_close`` dict
        :raises UserError: when no admission is selected, an admission
            fails the policy check, or the date range is inverted
        """
        for record in self.sudo():
            record._create_due_invoice()  # pylint: disable=protected-access
        return {"type": "ir.actions.act_window_close"}

    def _create_due_invoice(self):
        """Validate the input, then invoice every due payment term.

        Each selected admission invoices its uninvoiced payment terms
        whose estimated invoice date falls within the wizard range.

        :return: ``None``
        :raises UserError: when no admission is selected, an admission
            fails the policy check, or the date range is inverted
        """
        self.ensure_one()
        self._check_admissions()
        self._check_date_range()
        for admission in self.admission_ids:
            admission._create_due_invoice(  # pylint: disable=protected-access
                self.date_start, self.date_end
            )

    def _check_admissions(self):
        """Verify every selected admission may create due invoices.

        All admissions are checked before any is reported, so the error
        lists every problem at once.

        :return: ``None``
        :raises UserError: when nothing is selected, or when at least
            one admission fails ``create_invoice_ok``
        """
        self.ensure_one()
        if not self.admission_ids:
            error_message = (
                _(
                    """
Context: Create due invoice for admissions
Database ID: %s
Problem: No admission selected
Solution: Select at least one admission from the list view before running this wizard
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)
        problems = []
        for admission in self.admission_ids:
            if not admission.create_invoice_ok:
                problems.append(
                    _("- %s: not allowed to create due invoice (check state/policy)")
                    % admission.name
                )
        if problems:
            error_message = (
                _(
                    """
Context: Create due invoice for admissions
Database ID: %s
Problem: The following admission(s) are not allowed to create due invoice:
%s
Solution: Deselect the listed admission(s), or make sure they are open and allowed
by the create due invoice policy
"""
                )
                % (
                    self.id,
                    "\n".join(problems),
                )
            )
            raise UserError(error_message)

    def _check_date_range(self):
        """Verify the invoice date range is not inverted.

        An empty ``date_end`` is treated as today.

        :return: ``None``
        :raises UserError: when ``date_start`` is later than the
            effective end date
        """
        self.ensure_one()
        effective_end = self.date_end or fields.Date.context_today(self)
        if self.date_start and self.date_start > effective_end:
            error_message = (
                _(
                    """
Context: Create due invoice for admissions
Database ID: %s
Problem: Date Start '%s' is later than Date End '%s'
Solution: Choose a Date Start that is not later than Date End
"""
                )
                % (
                    self.id,
                    self.date_start,
                    effective_end,
                )
            )
            raise UserError(error_message)
