# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolHomeroomGenerate(YamlTransactionCase):
    def test_school_homeroom_generate(self):
        self.run_yaml_scenario("test_data_school_homeroom_generate.yaml")
