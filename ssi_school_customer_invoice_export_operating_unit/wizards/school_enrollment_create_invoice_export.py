# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class SchoolEnrollmentWizardCreateInvoiceExport(models.TransientModel):
    """
    Adds an explicit Operating Unit selection to the Create Invoice
    Export wizard for school enrollments. The selected operating unit
    restricts which of the collected moves are actually exported, and
    is propagated to the resulting ``customer_invoice_export``
    document.
    """

    _name = "school_enrollment.wizard_create_invoice_export"
    _inherit = "school_enrollment.wizard_create_invoice_export"

    operating_unit_id = fields.Many2one(
        string="Operating Unit",
        comodel_name="operating.unit",
        required=True,
        default=lambda self: self.env["res.users"].operating_unit_default_get(),
        help=(
            "Operating unit this export is being run for. Only "
            "invoices belonging to this operating unit are exported, "
            "and it is propagated to the resulting "
            "customer_invoice_export document. Defaults to the "
            "acting user's own default operating unit, not the "
            "operating unit of the selected enrollment(s), since the "
            "selection may span more than one operating unit."
        ),
    )

    def _filter_moves_by_operating_unit(self, moves):
        """Keep only the moves belonging to the selected operating unit.

        Moves without an operating unit are excluded rather than
        treated as unrestricted: the source moves are always school
        invoices, which are expected to always carry an operating
        unit once ``ssi_school_operating_unit`` is installed.

        :param moves: ``account.move`` recordset to filter
        :return: ``account.move`` recordset restricted to
            ``operating_unit_id``
        """
        self.ensure_one()
        return moves.filtered(
            lambda move: move.operating_unit_id == self.operating_unit_id
        )

    def _check_moves(self, moves):
        """Ensure at least one move survives the operating unit filter.

        Calls ``super()`` first, so the base "no exportable move"
        error is raised before this operating-unit-specific check
        runs.

        :param moves: ``account.move`` recordset collected from the
            selected enrollments, before operating unit filtering
        :raises UserError: when no move remains after filtering by
            ``operating_unit_id``
        """
        self.ensure_one()
        super()._check_moves(moves)
        if not self._filter_moves_by_operating_unit(moves):
            error_message = (
                _(
                    """
Context: Create invoice export for enrollments
Database ID: %s
Problem: No exportable move found for operating unit '%s'
Solution: Select a different operating unit, or select enrollment(s) invoiced under \
operating unit '%s'
"""
                )
                % (
                    self.id,
                    self.operating_unit_id.display_name,
                    self.operating_unit_id.display_name,
                )
            )
            raise UserError(error_message)

    def _prepare_invoice_export_data(self, moves):
        """Restrict ``source_move_ids`` to the selected operating unit.

        :param moves: ``account.move`` recordset collected from the
            selected enrollments, before operating unit filtering
        :return: dict of ``customer_invoice_export`` values, with
            ``source_move_ids`` restricted to ``operating_unit_id``
            and ``operating_unit_id`` itself added
        """
        self.ensure_one()
        res = super()._prepare_invoice_export_data(
            self._filter_moves_by_operating_unit(moves)
        )
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
