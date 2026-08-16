# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentGraduationOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Test Operating Unit storage on ``school_student_graduation``.

    Covers a graduation record created directly with an Operating Unit,
    confirming the value is stored as given.
    """

    def test_school_student_graduation_operating_unit(self):
        """Run the graduation Operating Unit storage scenario."""
        self.run_yaml_scenario(
            "test_data_school_student_graduation_operating_unit.yaml"
        )
