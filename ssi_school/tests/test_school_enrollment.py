# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentWorkflow(YamlTransactionCase):
    """Cover the document workflow of ``school_enrollment``.

    The scenarios walk an enrollment from draft through confirm,
    approve, invoicing and done, including a variant with a single
    manual payment term, and cover the onchange filling the receivable
    journal and account from the selected payment template.
    """

    def test_enrollment_workflow(self):
        """Run the enrollment workflow and onchange scenarios."""
        self.run_yaml_scenario("test_data_enrollment.yaml")
