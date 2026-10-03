# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionCreateStudent(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the Create Student Profile action of ``school_admission``."""

    def test_admission_create_student(self):
        """Run the create student profile scenarios."""
        self.run_yaml_scenario("test_data_admission_create_student.yaml")
