# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAcademicTerm(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``school_academic_term`` model.

    The scenarios exercise CRUD on a term, the first and last term flags
    computed inside its academic year, and the open, done and restart
    actions plus opening and closing enrollment on it.
    """

    def test_academic_term(self):
        """Run the academic term CRUD, flag and state action scenarios."""
        self.run_yaml_scenario("test_data_academic_term.yaml")
