# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolHomeroomGenerate(YamlTransactionCase):
    """Cover generating the enrollments of a homeroom.

    The scenarios exercise Fill Random followed by the generation, the
    eligibility rules on a non first term, the remaining capacity limit,
    the reconciliation of the draft enrollments on a regeneration, and
    the guard protecting an enrollment that already left draft.
    """

    def test_school_homeroom_generate(self):
        """Run the fill random, capacity and regeneration scenarios."""
        self.run_yaml_scenario("test_data_school_homeroom_generate.yaml")
