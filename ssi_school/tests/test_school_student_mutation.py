# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentMutation(YamlTransactionCase):
    """Cover the class mutation document of a student.

    The scenarios exercise the draft mutation, its onchanges, the
    confirm, approve and done workflow moving the student to another
    grade class, the constraints guarding the destination, the
    enrollment and the destination capacity, cancelling a draft, and
    undoing a completed mutation with a reverse one.
    """

    def test_school_student_mutation(self):
        """Run the class mutation workflow, cancel and undo scenarios."""
        self.run_yaml_scenario("test_data_school_student_mutation.yaml")
