# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentFamily(YamlTransactionCase):
    """Cover the family data shared by a student and its contact.

    The scenarios check that family data already held by the contact
    shows up on a student created from it, that writing a parent or a
    guardian on either side propagates to the other, and that clearing
    a parent on the contact clears it on the student too.
    """

    def test_student_family(self):
        """Run the family data propagation scenarios."""
        self.run_yaml_scenario("test_data_school_student_family.yaml")
