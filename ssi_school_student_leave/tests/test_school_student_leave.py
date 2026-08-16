# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentLeave(YamlTransactionCase):
    """Test the Student Leave of Absence document.

    Runs the YAML scenarios covering the full leave life cycle: the
    draft document created for an enrolled student, the confirm and
    approve workflow that auto-completes the leave to done and moves
    the student to the on_leave state, the return that re-enrolls the
    student, and the two constraints that reject a leave for a student
    who is not enrolled and a second active leave for the same student.
    """

    def test_school_student_leave(self):
        """Run every Student Leave scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_student_leave.yaml")
