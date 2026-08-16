# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentGraduationBatch(YamlTransactionCase):
    """Test the Student Graduation Batch document.

    Runs the YAML scenarios covering the batch life cycle: populating
    the batch lines from the academic year, academic term and grade
    filters, the confirm and approve workflow that completes the batch
    to done and generates one done Student Graduation document per
    line, and the two completion checks that reject a batch without
    any student line and a batch whose lines point at students who are
    no longer enrolled.
    """

    def test_school_student_graduation_batch(self):
        """Run every Student Graduation Batch scenario in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_student_graduation_batch.yaml")
