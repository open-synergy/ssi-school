# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolTeacher(YamlTransactionCase):  # pylint: disable=too-few-public-methods
    """Cover the ``school_teacher`` model and its home address.

    The scenarios exercise CRUD on a teacher, changing the employee it
    points to, the fields related from the home address contact, and
    writing personal information back to that contact.
    """

    def test_teacher(self):
        """Run the teacher CRUD and home address relation scenarios."""
        self.run_yaml_scenario("test_data_teacher.yaml")
