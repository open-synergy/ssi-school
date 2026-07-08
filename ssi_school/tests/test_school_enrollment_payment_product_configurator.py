# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentProductConfigurator(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    def test_enrollment_payment_product_configurator(self):
        self.run_yaml_scenario("test_data_enrollment_payment_product_configurator.yaml")
