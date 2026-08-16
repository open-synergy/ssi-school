# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentLeaveOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Test the ``operating_unit_id`` field on ``school_student_leave``.

    Covers the field added by this glue module and confirms it is
    stored as given when a student leave is created.
    """

    def test_school_student_leave_operating_unit(self):
        """Confirm ``operating_unit_id`` persists on student leave.

        Runs the scenario that creates a student leave with an
        explicit operating unit, then searches for the record by
        that same ``operating_unit_id`` to confirm it was stored.
        """
        self.run_yaml_scenario("test_data_school_student_leave_operating_unit.yaml")
