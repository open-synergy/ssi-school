# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolAdmissionPaymentTerm(models.Model):
    """
    Extends School Admission Payment Term to propagate
    operating_unit_id from the parent admission to the generated invoice.
    """

    _name = "school_admission_payment_term"
    _inherit = "school_admission_payment_term"

    def _prepare_invoice_data(self):
        res = super()._prepare_invoice_data()
        res["operating_unit_id"] = self.admission_id.operating_unit_id.id
        return res
