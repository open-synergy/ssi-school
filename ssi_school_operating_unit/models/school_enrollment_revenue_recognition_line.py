# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolEnrollmentRevenueRecognitionLine(models.Model):
    _inherit = "school_enrollment_revenue_recognition_line"

    def _prepare_standard_ml(self, direction):
        """Add the parent enrollment's own operating unit to the values.

        Extension point (``mixin.account_move_double_line``): both the
        debit and credit journal item of the Revenue Recognition move
        must always carry the parent enrollment's own
        ``operating_unit_id`` -- never the acting user's default
        operating unit.

        :param direction: ``"debit"`` or ``"credit"``
        :return: dict of ``account.move.line`` create values
        """
        result = super()._prepare_standard_ml(direction)
        result["operating_unit_id"] = self.enrollment_id.operating_unit_id.id
        return result
