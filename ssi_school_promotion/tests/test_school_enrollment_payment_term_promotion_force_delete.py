# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentTermPromotionForceDelete(YamlTransactionCase):
    """Scenario tests for the force delete guard of usage allocations."""

    def test_school_enrollment_payment_term_promotion_force_delete(self):
        """Run the force delete invoice guard scenario."""
        self.run_yaml_scenario(
            "test_data_school_enrollment_payment_term_promotion_force_delete.yaml"
        )
