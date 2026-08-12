# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentDatePattern(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the invoice and due dates computed on a payment term.

    The scenarios check that a term carrying a duration derives its
    estimated invoice and due dates from that duration, and that a term
    without any duration leaves both dates empty.
    """

    def test_enrollment_payment_date_pattern(self):
        """Run the payment term date computation scenarios."""
        self.run_yaml_scenario("test_data_enrollment_payment_date_pattern.yaml")
