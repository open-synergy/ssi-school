# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrEmployee(YamlTransactionCase):  # pylint: disable=too-few-public-methods
    """Cover the teacher record derived from an ``hr.employee``.

    The scenarios check that saving an employee creates its
    ``school_teacher`` counterpart, how the teacher code falls back when
    the employee carries no barcode, and that the creation is idempotent
    so an existing teacher is never duplicated.
    """

    def test_create_teacher_from_employee(self):
        """Run the employee to teacher creation scenarios."""
        self.run_yaml_scenario("test_data_hr_employee.yaml")
