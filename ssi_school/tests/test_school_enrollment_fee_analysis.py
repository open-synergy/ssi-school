# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentFeeAnalysis(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the fee analysis rows derived from enrollment payments.

    The scenarios check that a payment term detail produces one analysis
    row carrying the right amount and dimensions, that two terms keep
    their own rows instead of being aggregated, and that the row
    disappears once the detail is unlinked.
    """

    def test_school_enrollment_fee_analysis(self):
        """Run the fee analysis row creation and removal scenarios."""
        self.run_yaml_scenario("test_data_enrollment_fee_analysis.yaml")
