# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentRevenueRecognitionOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the Revenue Recognition move's own operating unit.

    Covers the move header and every journal item carrying the
    enrollment's own ``operating_unit_id`` regardless of the acting
    user's default operating unit, and the negative path where
    Revenue Recognition is disabled.
    """

    def test_school_enrollment_revenue_recognition_operating_unit(self):
        """Run every Revenue Recognition operating unit scenario."""
        self.run_yaml_scenario(
            "test_data_school_enrollment_revenue_recognition_operating_unit.yaml"
        )
