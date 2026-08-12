# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolGrade(YamlTransactionCase):  # pylint: disable=too-few-public-methods
    """Cover the ``school_grade`` model.

    The scenarios exercise CRUD on a grade, editing its sequence, and
    the previous and next grade chain computed from that sequence, which
    stays scoped to a single grade type.
    """

    def test_grade(self):
        """Run the grade CRUD and previous/next grade chain scenarios."""
        self.run_yaml_scenario("test_data_grade.yaml")
