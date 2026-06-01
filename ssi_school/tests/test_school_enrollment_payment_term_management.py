# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentTermManagement(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    def test_enrollment_payment_term_management(self):
        self.run_yaml_scenario("test_data_enrollment_payment_term_management.yaml")
