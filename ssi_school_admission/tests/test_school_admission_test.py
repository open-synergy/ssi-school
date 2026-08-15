# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionTest(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``school_admission_test`` document workflow."""

    def test_admission_test_workflow(self):
        """Run the admission test workflow scenarios.

        Covers the full confirm/approve/open/done flow, creation without
        an admission form, and the uniqueness constraint that lets one
        admission form yield at most one admission test.
        """
        self.run_yaml_scenario("test_data_admission_test_workflow.yaml")
