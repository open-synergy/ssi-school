# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentProductConfigurator(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the products allowed on a payment term detail.

    The scenarios exercise the manual, domain and Python code selection
    strategies on both the payment template detail and the enrollment
    payment term detail, including an empty manual selection and a
    detail whose enrollment has no payment template at all.
    """

    def test_enrollment_payment_product_configurator(self):
        """Run the allowed product selection strategy scenarios."""
        self.run_yaml_scenario("test_data_enrollment_payment_product_configurator.yaml")
