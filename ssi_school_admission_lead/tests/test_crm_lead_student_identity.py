# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCrmLeadStudentIdentity(YamlTransactionCase):
    """Covers the student identity fields related from the contact."""

    def test_crm_lead_student_identity(self):
        """Run the lead student identity write-through scenario."""
        self.run_yaml_scenario("test_data_lead_student_identity.yaml")
