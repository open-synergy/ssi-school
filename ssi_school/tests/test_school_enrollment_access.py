# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentAccess(YamlTransactionCase):
    """Cover the record rules of the school transactional documents.

    The scenarios check that an administrator can read and run the
    confirm and approve workflow on an enrollment, a homeroom and a
    student mutation created by another user, while a plain internal
    user stays restricted to its own enrollment.
    """

    def test_school_enrollment_access(self):
        """Run the administrator and restricted user access scenarios."""
        self.run_yaml_scenario("test_data_school_enrollment_access.yaml")
