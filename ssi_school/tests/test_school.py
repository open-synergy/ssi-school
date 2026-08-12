# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchool(YamlTransactionCase):
    """Cover the ``school`` model and its placement in the org chart.

    The scenarios exercise CRUD on a school, editing its grade type,
    attaching it either directly to a center or to a branch, and the
    onchange clearing the branch once the center no longer owns it.
    """

    def test_school(self):
        """Run the school CRUD, placement and onchange scenarios."""
        self.run_yaml_scenario("test_data_school.yaml")
