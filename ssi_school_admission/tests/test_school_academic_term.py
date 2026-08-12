# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAcademicTermAdmission(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the admission flag added to ``school_academic_term``."""

    def test_school_academic_term_admission(self):
        """Run the academic term admission scenario."""
        self.run_yaml_scenario("test_data_academic_term.yaml")
