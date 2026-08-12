# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolHomeroom(YamlTransactionCase):
    """Cover the ``school_homeroom`` document and its candidates.

    The scenarios exercise the draft homeroom, its relation to the
    generated enrollments, the confirm, approve and open workflow, the
    capacity filled by the grade class onchange, and the way Fill Random
    picks candidates on a first and on a non first academic term.
    """

    def test_school_homeroom(self):
        """Run the homeroom draft, workflow and candidate scenarios."""
        self.run_yaml_scenario("test_data_school_homeroom.yaml")
