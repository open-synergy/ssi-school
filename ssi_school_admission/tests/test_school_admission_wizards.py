# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionWizards(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the wizards creating an admission from form and test."""

    def test_admission_wizards(self):
        """Run the admission wizards scenario."""
        self.run_yaml_scenario("test_data_admission_wizards.yaml")
