# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentIntegrity(YamlTransactionCase):
    """Cover the constraints rejecting inconsistent enrollment data.

    The scenarios exercise the term versus academic year check, the
    grade class versus school check, the enrollment window of the term,
    the ban on two active enrollments for one student, and the seat
    limit of a capped grade class.
    """

    def test_school_enrollment_integrity(self):
        """Run the enrollment consistency and capacity scenarios."""
        self.run_yaml_scenario("test_data_enrollment_integrity.yaml")
