# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudent(YamlTransactionCase):
    """Cover the ``school_student`` model.

    The scenarios exercise CRUD on a student, the initial, current and
    next grade computed from its enrollments, the active enrollment, the
    state actions, the rules on duplicate codes within a school and the
    school onchange clearing the initial grade.
    """

    def test_student(self):
        """Run the student CRUD, compute, state and duplicate scenarios."""
        self.run_yaml_scenario("test_data_student.yaml")
