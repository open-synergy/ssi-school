# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentGraduation(YamlTransactionCase):
    """Test the Student Graduation document.

    Runs the YAML scenarios covering the full graduation life cycle:
    the draft document created for an enrolled student together with
    the active enrollment snapshot taken from that student, the
    confirm and approve workflow that completes the document to done,
    numbers it, moves the student to the graduate state and marks the
    enrollment academic year result as graduate, and the two
    constraints that reject a confirmation for a student who is no
    longer enrolled and a second active graduation for the same
    student.
    """

    def test_school_student_graduation(self):
        """Run every Student Graduation scenario in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_student_graduation.yaml")
