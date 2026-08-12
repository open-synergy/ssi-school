# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolGradeClass(YamlTransactionCase):
    """Cover the ``school_grade_class`` model.

    The scenarios exercise CRUD on a class, the grade type computed from
    its school, the student count and available seat when no enrollment
    exists yet, and the onchange clearing the grade when the school
    changes.
    """

    def test_grade_class(self):
        """Run the grade class CRUD, compute and onchange scenarios."""
        self.run_yaml_scenario("test_data_grade_class.yaml")
