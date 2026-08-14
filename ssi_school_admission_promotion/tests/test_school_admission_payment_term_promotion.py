# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionPaymentTermPromotion(YamlTransactionCase):
    """Scenario tests for ``mixin.promotion_object`` on
    ``school_admission_payment_term``.
    """

    def test_school_admission_payment_term_promotion(self):
        """Run the Populate Allocation / approve / locked / Voucher
        User / negative path scenarios against an admission payment
        term.
        """
        self.run_yaml_scenario("test_data_school_admission_payment_term_promotion.yaml")
