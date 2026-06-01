# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentResults(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    def test_enrollment_results(self):
        self.run_yaml_scenario("test_data_enrollment_results.yaml")
