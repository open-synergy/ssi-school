# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolHealth(YamlTransactionCase):
    """Cover the ``school_student`` health fields and their history lines.

    Exercises the related One2many fields (height, weight, head
    circumference, allergy, disease history) exposed on
    ``school_student`` through the linked ``res.partner`` contact.
    """

    def test_school_health(self):
        """Run the school health scenario."""
        self.run_yaml_scenario("test_data_school_health.yaml")
