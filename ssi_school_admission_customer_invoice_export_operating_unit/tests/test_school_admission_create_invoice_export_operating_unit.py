# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionCreateInvoiceExportOperatingUnit(YamlTransactionCase):
    """Cover the Operating Unit selection on the Create Invoice Export
    wizard for school admissions.

    Exercises every behavior scenario -- default value, filtering by
    operating unit, mismatched operating unit, and the required-field
    check -- as YAML, since ``operating_unit_id`` is required at the
    field level and already appears (visible, not view-restricted) on
    the wizard's only form, so the required-field check is reachable
    through the standard ``action: form`` save flow instead of any
    Python-only escape hatch.
    """

    def test_school_admission_create_invoice_export_operating_unit(self):
        """Run the operating unit selection scenarios."""
        self.run_yaml_scenario(
            "test_data_school_admission_create_invoice_export_operating_unit.yaml"
        )
