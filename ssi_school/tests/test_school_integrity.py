# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolIntegrity(YamlTransactionCase):
    """Cover the constraint tying a school branch to its own center.

    The scenarios exercise the rejection of a branch owned by another
    company, both when the school is created and when an existing school
    is written.
    """

    def test_school_integrity(self):
        """Run the school branch versus center integrity scenarios."""
        self.run_yaml_scenario("test_data_school_integrity.yaml")
