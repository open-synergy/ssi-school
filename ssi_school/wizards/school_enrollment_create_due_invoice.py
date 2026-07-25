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
        res = super().default_get(fields_list)
        if self.env.context.get("active_model") == "school_enrollment":
            active_ids = self.env.context.get("active_ids", [])
            res["enrollment_ids"] = [(6, 0, active_ids)]
        return res

    def action_create_due_invoice(self):
        for record in self.sudo():
            record._create_due_invoice()  # pylint: disable=protected-access
        return {"type": "ir.actions.act_window_close"}

    def _create_due_invoice(self):
        self.ensure_one()
        self._check_enrollments()
        self._check_date_range()
        for enrollment in self.enrollment_ids:
            enrollment._create_due_invoice(  # pylint: disable=protected-access
                self.date_start, self.date_end
            )

    def _check_enrollments(self):
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
