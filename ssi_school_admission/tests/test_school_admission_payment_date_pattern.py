# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionPaymentDatePattern(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the invoice/due date pattern of admission payment terms."""

    def test_admission_payment_date_pattern(self):
        """Run the admission payment date pattern scenario."""
        self.run_yaml_scenario("test_data_admission_payment_date_pattern.yaml")
