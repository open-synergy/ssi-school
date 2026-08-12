# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentAddendum(YamlTransactionCase):
    """Cover the addendum flow of an already open enrollment.

    Opening an enrollment locks its payment terms and details, so the
    scenarios check that locked records reject both write and unlink,
    that closing an addendum locks only the terms added afterwards, and
    that the addendum can be repeated several times on one enrollment.
    """

    def test_enrollment_addendum(self):
        """Run every payment term locking scenario of the addendum."""
        self.run_yaml_scenario("test_data_enrollment_addendum.yaml")
