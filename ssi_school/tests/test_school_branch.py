# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolBranch(YamlTransactionCase):  # pylint: disable=too-few-public-methods
    """Cover the ``school_branch`` model.

    The scenarios exercise CRUD on a branch, creating it with an
    explicit center, archiving it, and the reverse relation counting the
    school units that belong to it.
    """

    def test_school_branch(self):
        """Run the branch CRUD, archive and school unit count scenarios."""
        self.run_yaml_scenario("test_data_school_branch.yaml")
