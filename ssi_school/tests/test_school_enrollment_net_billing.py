# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentNetBilling(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the net billing breakdown of the enrollment header.

    The scenarios exercise ``amount_deduction``, ``amount_net``,
    ``amount_deducted``, ``amount_deduction_pending``,
    ``amount_payment``, ``amount_other_credit``, and
    ``amount_outstanding`` on ``school_enrollment``: a bank payment,
    a credit from a general journal, a term without invoice, and a
    cancelled term with a paid invoice.
    """

    def test_enrollment_net_billing(self):
        """Run every net billing scenario against the fixtures."""
        self.run_yaml_scenario("test_data_enrollment_net_billing.yaml")
