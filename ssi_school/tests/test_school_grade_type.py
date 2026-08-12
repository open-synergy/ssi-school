# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolGradeType(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``school_grade_type`` model.

    The scenarios exercise the create, edit name, edit sequence and
    delete flows of a grade type, the master data every grade and school
    is classified under.
    """

    def test_grade_type(self):
        """Run the grade type CRUD scenarios."""
        self.run_yaml_scenario("test_data_grade_type.yaml")
