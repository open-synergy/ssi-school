# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionPaymentProductConfigurator(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the product configurator of admission payment terms."""

    def test_admission_payment_product_configurator(self):
        """Run the admission payment product configurator scenario."""
        self.run_yaml_scenario("test_data_admission_payment_product_configurator.yaml")
