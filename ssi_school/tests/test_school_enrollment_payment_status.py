# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentStatus(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the enrollment-level payment aggregate fields.

    The scenarios exercise ``amount_total``, ``amount_paid``,
    ``amount_residual``, and ``payment_status`` on
    ``school_enrollment`` across every ``payment_status`` value:
    two uninvoiced terms (``unpaid``), one paid and one uninvoiced
    term (``partial``), two fully paid terms (``paid``), no payment
    term at all (``no_payment``), a fully voided term (``no_payment``
    via exclusion), and a cancelled enrollment (``no_payment`` even
    after amounts were realized).
    """

    def test_enrollment_payment_status(self):
        """Run every payment-status scenario against the fixtures."""
        self.run_yaml_scenario("test_data_enrollment_payment_status.yaml")
