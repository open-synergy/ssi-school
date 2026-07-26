# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SchoolEnrollmentWizardCreateInvoiceExport(models.TransientModel):
    """
    Wizard that collects the unpaid customer invoices generated from the
    payment terms of one or more selected enrollments and exports them
    into a draft ``customer_invoice_export`` document, ready to be
    confirmed. Every selected enrollment must be allowed by the
    create_invoice_export_ok policy (state and group, configurable via
    Policy Template). All enrollments are validated, and the created
    document must have at least one summary row, before the wizard
    completes.
    """

    _name = "school_enrollment.wizard_create_invoice_export"
    _description = "Create Invoice Export for Enrollment Payment Terms"

    enrollment_ids = fields.Many2many(
        string="Enrollments",
        comodel_name="school_enrollment",
        relation="rel_school_enrollment_create_invoice_export",
        column1="wizard_id",
        column2="enrollment_id",
        readonly=True,
        help="Enrollments whose unpaid invoices will be exported.",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="customer_invoice_export_type",
        required=True,
        help=(
            "Export type that determines the product criteria, the "
            "parser code, and the default output format of the "
            "resulting document."
        ),
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=lambda self: fields.Date.context_today(self),
        help="Date of the resulting customer invoice export document.",
    )
    output_format = fields.Selection(
        string="Output Format",
        selection=[
            ("csv", "CSV"),
            ("xlsx", "XLSX"),
            ("txt", "TXT"),
        ],
        required=True,
        help=(
            "File format of the resulting document. Automatically "
            "proposed from the selected Type."
        ),
    )
    date_start = fields.Date(
        string="Date Start",
        help=(
            "Lower bound (inclusive) on invoice date, passed as-is to "
            "the resulting document. Leave empty for no lower bound."
        ),
    )
    date_end = fields.Date(
        string="Date End",
        help=(
            "Upper bound (inclusive) on invoice date, passed as-is to "
            "the resulting document. Leave empty for no upper bound."
        ),
    )

    @api.model
    def default_get(self, fields_list):
        """Pre-fill ``enrollment_ids`` from the calling window action.

        :param fields_list: fields requested by the view
        :return: dict of default values
        """
        res = super().default_get(fields_list)
        if self.env.context.get("active_model") == "school_enrollment":
            active_ids = self.env.context.get("active_ids", [])
            res["enrollment_ids"] = [(6, 0, active_ids)]
        return res

    @api.onchange("type_id")
    def onchange_output_format(self):
        """Propose the selected Type's default output format."""
        self.output_format = (
            self.type_id.default_output_format if self.type_id else False
        )

    def action_create_invoice_export(self):
        """Create the customer invoice export document and open it.

        :return: an ``ir.actions.act_window`` opening the created
            ``customer_invoice_export`` document in form view
        """
        export = self.env["customer_invoice_export"]
        for record in self.sudo():
            export = record._create_invoice_export()  # pylint: disable=protected-access
        return {
            "type": "ir.actions.act_window",
            "res_model": "customer_invoice_export",
            "res_id": export.id,
            "view_mode": "form",
            "target": "current",
        }

    def _create_invoice_export(self):
        """Build the ``customer_invoice_export`` document for this wizard.

        Validates the selected enrollments, collects the unpaid invoice
        moves from all of them via
        ``school_enrollment._get_exportable_move``, creates the export
        document with those moves in ``source_move_ids``, populates it,
        and verifies at least one summary row was produced.

        :raises UserError: no enrollment selected, an enrollment is not
            allowed by the create invoice export policy, no exportable
            move was found, or the populated document has no summary
            row
        :return: the created ``customer_invoice_export`` record
        """
        self.ensure_one()
        self._check_enrollments()
        moves = self.env["account.move"]
        for enrollment in self.enrollment_ids:
            moves |= (
                enrollment._get_exportable_move()
            )  # pylint: disable=protected-access
        self._check_moves(moves)
        export = self.env["customer_invoice_export"].create(
            self._prepare_invoice_export_data(moves)
        )
        export.action_populate()
        self._check_summary(export)
        return export

    def _prepare_invoice_export_data(self, moves):
        """Build the ``customer_invoice_export`` creation values.

        :param moves: ``account.move`` recordset collected from the
            selected enrollments
        :return: dict of ``customer_invoice_export`` values
        """
        self.ensure_one()
        return {
            "type_id": self.type_id.id,
            "date": self.date,
            "output_format": self.output_format,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "source_move_ids": [(6, 0, moves.ids)],
        }

    def _check_enrollments(self):
        """Validate the selected enrollments before exporting.

        :raises UserError: no enrollment selected, or one or more
            selected enrollments are not allowed by the create invoice
            export policy
        """
        self.ensure_one()
        if not self.enrollment_ids:
            error_message = (
                _(
                    """
Context: Create invoice export for enrollments
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
            if not enrollment.create_invoice_export_ok:
                problems.append(
                    _("- %s: not allowed to create invoice export (check state/policy)")
                    % enrollment.name
                )
        if problems:
            error_message = (
                _(
                    """
Context: Create invoice export for enrollments
Database ID: %s
Problem: The following enrollment(s) are not allowed to create invoice export:
%s
Solution: Deselect the listed enrollment(s), or make sure they are open/done and allowed
by the create invoice export policy
"""
                )
                % (
                    self.id,
                    "\n".join(problems),
                )
            )
            raise UserError(error_message)

    def _check_moves(self, moves):
        """Ensure at least one exportable move was found.

        :param moves: ``account.move`` recordset collected from the
            selected enrollments
        :raises UserError: when ``moves`` is empty
        """
        self.ensure_one()
        if not moves:
            error_message = (
                _(
                    """
Context: Create invoice export for enrollments
Database ID: %s
Problem: No exportable move found on the selected enrollment(s)
Solution: Select enrollment(s) that have at least one payment term with an unpaid \
(open) customer invoice
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)

    def _check_summary(self, export):
        """Ensure the populated document has at least one summary row.

        :param export: the created ``customer_invoice_export`` record
        :raises UserError: when ``summary_ids`` is empty after
            ``action_populate``
        """
        self.ensure_one()
        if not export.summary_ids:
            error_message = (
                _(
                    """
Context: Create invoice export for enrollments
Database ID: %s
Problem: No summary row was produced for the exported invoices
Solution: Check the Journal/Partner/Product criteria on Type '%s'
"""
                )
                % (self.id, export.type_id.display_name)
            )
            raise UserError(error_message)
