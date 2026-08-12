# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentCopyPaymentTerm(YamlTransactionCase):
    """Cover the wizard copying payment terms between enrollments.

    The scenarios exercise the replace, add and multi target modes, and
    the guards refusing to copy into a target that left draft or whose
    grade differs from the source.
    """

    def test_enrollment_copy_payment_term(self):
        """Run every copy payment term scenario of the wizard."""
        self.run_yaml_scenario("test_data_enrollment_copy_payment_term.yaml")
