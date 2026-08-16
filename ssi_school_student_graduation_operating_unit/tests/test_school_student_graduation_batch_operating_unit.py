# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentGraduationBatchOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Test Operating Unit propagation on ``school_student_graduation_batch``.

    Covers a batch created with an Operating Unit that, once approved,
    generates a ``school_student_graduation`` record inheriting the same
    Operating Unit.
    """

    def test_school_student_graduation_batch_operating_unit(self):
        """Run the batch-to-graduation Operating Unit propagation scenario."""
        self.run_yaml_scenario(
            "test_data_school_student_graduation_batch_operating_unit.yaml"
        )
