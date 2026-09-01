# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionPaymentTermVoided(YamlTransactionCase):
    """Behaviour of the ``voided`` flag on payment term detail lines."""

    def test_admission_payment_term_voided(self):
        """Run every voided-flag scenario against the YAML fixtures."""
        self.run_yaml_scenario("test_data_admission_payment_term_voided.yaml")
