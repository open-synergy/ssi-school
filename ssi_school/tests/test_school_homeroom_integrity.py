# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolHomeroomIntegrity(YamlTransactionCase):
    """Cover the constraints rejecting inconsistent homeroom data.

    The scenarios exercise the check tying the academic term to the
    selected academic year, and the one tying the grade class to the
    selected school.
    """

    def test_school_homeroom_integrity(self):
        """Run the homeroom term, year and grade class scenarios."""
        self.run_yaml_scenario("test_data_school_homeroom_integrity.yaml")
