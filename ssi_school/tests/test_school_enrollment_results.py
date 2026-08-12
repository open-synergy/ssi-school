# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentResults(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the academic year result closing an open enrollment.

    The scenarios exercise the passed, failed, drop out and graduate
    outcomes, checking that each one moves the enrollment to done with
    the matching result and leaves the student in the expected state.
    """

    def test_enrollment_results(self):
        """Run the passed, failed, drop out and graduate scenarios."""
        self.run_yaml_scenario("test_data_enrollment_results.yaml")
