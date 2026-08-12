# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentRestartUnlock(YamlTransactionCase):
    """Cover unlocking the payment terms when an enrollment restarts.

    The scenarios check that a restart makes the locked terms and their
    details editable again, that the lock stays on when no cancel
    happened, that payment terms can be copied into a restarted
    enrollment, and that the cancel is blocked while a customer invoice
    still exists.
    """

    def test_enrollment_restart_unlock(self):
        """Run every restart scenario for terms, details and cancel."""
        self.run_yaml_scenario("test_data_enrollment_restart_unlock.yaml")
