# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SchoolEnrollmentWizardCreateDueInvoice(models.TransientModel):
    """
    Wizard that creates invoices for all uninvoiced payment terms whose
    estimated invoice date (date_invoice) falls within a given date range, for
    one or more enrollments selected from the school_enrollment list view or
    from a single enrollment's form. Every selected enrollment must be allowed
    by the create_invoice_ok policy (state and group, configurable via Policy
    Template). All enrollments are validated before any invoice is created.
    """

    _name = "school_enrollment.wizard_create_due_invoice"
    _description = "Create Due Invoice for Enrollment Payment Terms"

    enrollment_ids = fields.Many2many(
        string="Enrollments",
        comodel_name="school_enrollment",
        relation="rel_school_enrollment_create_due_invoice",
        column1="wizard_id",
        column2="enrollment_id",
        readonly=True,
        help="Enrollments whose due payment terms will be invoiced.",
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
        """Preload the enrollments selected in the calling view.

        Overridden so the user does not have to re-pick records already
        selected: when the wizard is opened from ``school_enrollment``,
        ``active_ids`` becomes the value of ``enrollment_ids``.

        :param fields_list: list of field names Odoo asks defaults for
        :return: dict of default values
        """
        res = super().default_get(fields_list)
        if self.env.context.get("active_model") == "school_enrollment":
            active_ids = self.env.context.get("active_ids", [])
            res["enrollment_ids"] = [(6, 0, active_ids)]
        return res

    def action_create_due_invoice(self):
        """Invoice the due payment terms of every selected enrollment.

        Triggered by the wizard button. Delegates to ``_create_due_invoice``
        for each wizard record, then closes the dialog. Customer invoices
        are created and linked back to the payment terms.

        :return: an ``ir.actions.act_window_close`` action
        :raises UserError: when no enrollment is selected, an enrollment is
            rejected by the policy, or the date range is inverted
        """
        for record in self.sudo():
            record._create_due_invoice()  # pylint: disable=protected-access
        return {"type": "ir.actions.act_window_close"}

    def _create_due_invoice(self):
        """Run the invoicing for each enrollment held by this wizard.

        Both guards run first, so a rejected enrollment or an inverted date
        range aborts the whole run before any invoice is created. The actual
        work is delegated to ``school_enrollment._create_due_invoice``, which
        picks the uninvoiced payment terms whose ``date_invoice`` falls in
        the requested range.

        :raises UserError: propagated from ``_check_enrollments`` or
            ``_check_date_range``
        """
        self.ensure_one()
        self._check_enrollments()
        self._check_date_range()
        for enrollment in self.enrollment_ids:
            enrollment._create_due_invoice(  # pylint: disable=protected-access
                self.date_start, self.date_end
            )

    def _check_enrollments(self):
        """Validate the selected enrollments before any invoice is made.

        Rejects the run when nothing is selected, and when an enrollment has
        ``create_invoice_ok`` False (state or group not allowed by the Policy
        Template). All offending enrollments are collected so the user sees
        them in a single message.

        :raises UserError: when no enrollment is selected, or at least one
            enrollment is not allowed to create a due invoice
        """
        self.ensure_one()
        if not self.enrollment_ids:
            error_message = (
                _(
                    """
Context: Create due invoice for enrollments
Database ID: %s
Problem: No enrollment selected
Solution: Select at least one enrollment from the list view before running this wizard
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)
        problems = []
        for enrollment in self.enrollment_ids:
            if not enrollment.create_invoice_ok:
                problems.append(
                    _("- %s: not allowed to create due invoice (check state/policy)")
                    % enrollment.name
                )
        if problems:
            error_message = (
                _(
                    """
Context: Create due invoice for enrollments
Database ID: %s
Problem: The following enrollment(s) are not allowed to create due invoice:
%s
Solution: Deselect the listed enrollment(s), or make sure they are open and allowed
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
        """Reject an inverted invoicing window.

        An empty ``date_end`` means "up to today", so the comparison uses
        that effective end instead of skipping the check.

        :raises UserError: when ``date_start`` is later than the effective
            end date
        """
        self.ensure_one()
        effective_end = self.date_end or fields.Date.context_today(self)
        if self.date_start and self.date_start > effective_end:
            error_message = (
                _(
                    """
Context: Create due invoice for enrollments
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
