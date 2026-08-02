# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCrmLeadStudentNisn(YamlTransactionCase):
    """Test the ``student_nisn`` field on ``crm.lead``.

    The field reads and writes ``res.partner.nisn`` of the prospective
    student through ``sudo()``, so that an admission officer without the
    partner ID number configurator group can still maintain the NISN from
    the lead form.
    """

    def test_crm_lead_student_nisn(self):
        """Run the YAML scenarios covering ``student_nisn``."""
        self.run_yaml_scenario("test_data_crm_lead_student_nisn.yaml")
