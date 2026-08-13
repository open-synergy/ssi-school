# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentTransferIn(YamlTransactionCase):
    """Cover transfer-in enrollment for ``school_student``/``school_enrollment``.

    Verifies that a student flagged ``is_transfer_in`` can be enrolled into
    any grade of any term (not only the grade matched by the computed
    current/next grade), and that a regular student's eligibility is
    unaffected.
    """

    def test_transfer_in_allowed_on_non_first_term_middle_grade(self):
        """Run the transfer-in enrollment eligibility scenario."""
        self.run_yaml_scenario("test_data_student_transfer_in.yaml")
