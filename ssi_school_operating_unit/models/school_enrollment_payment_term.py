# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolEnrollmentPaymentTerm(models.Model):
    """
    Extends School Enrollment Payment Term to propagate
    operating_unit_id from the parent enrollment to the generated invoice.
    """

    _name = "school_enrollment_payment_term"
    _inherit = "school_enrollment_payment_term"

    def _prepare_invoice_data(self):
        res = super()._prepare_invoice_data()
        res["operating_unit_id"] = self.enrollment_id.operating_unit_id.id
        return res
