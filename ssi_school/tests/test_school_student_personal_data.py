# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentPersonalData(YamlTransactionCase):
    """Cover the personal data shared by a student and its contact.

    The scenarios check the write-through of the scalar fields from the
    student to the contact, the read back in the other direction, a bank
    account line created through the student, and the non-stored age
    following the live contact value.
    """

    def test_student_personal_data(self):
        """Run the personal data write-through and read back scenarios."""
        self.run_yaml_scenario("test_data_student_personal_data.yaml")
