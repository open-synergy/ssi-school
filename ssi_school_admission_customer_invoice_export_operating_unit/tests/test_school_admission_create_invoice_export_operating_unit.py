# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestSchoolAdmissionCreateInvoiceExportOperatingUnit(YamlTransactionCase):
    """Cover the Operating Unit selection on the Create Invoice Export
    wizard for school admissions.

    Exercises the YAML behavior scenarios (default value, filtering by
    operating unit, mismatched operating unit) and the Python-only
    required-field scenario below.
    """

    def test_school_admission_create_invoice_export_operating_unit(self):
        """Run the operating unit selection scenarios."""
        self.run_yaml_scenario(
            "test_data_school_admission_create_invoice_export_operating_unit.yaml"
        )

    @mute_logger("odoo.sql_db")
    def test_operating_unit_id_is_required(self):
        """Reject creating the wizard without an operating unit.

        Pure Python, trigger P5 (L-22): ``operating_unit_id`` is a
        plain ``required=True`` Many2one, so leaving it empty is
        enforced by the database NOT NULL constraint, which raises
        ``psycopg2.IntegrityError`` -- an exception type outside the
        12 names ``expect_error`` recognizes, so this cannot be
        written as a YAML ``expect_error`` step. ``mute_logger``
        silences the expected PostgreSQL ERROR log line so
        ``oca_checklog_odoo`` does not fail the build over an error
        this test deliberately triggers. ``admission_ids`` is not
        required at the model level, so no admission needs to be
        built to isolate the NOT NULL violation to
        ``operating_unit_id``.
        """
        export_type = self.env["customer_invoice_export_type"].create(
            {
                "name": "Export Type ROU1",
                "code": "ETYROU1",
                "default_output_format": "csv",
            }
        )
        with self.assertRaises(IntegrityError):
            self.env["school_admission.wizard_create_invoice_export"].create(
                {
                    "type_id": export_type.id,
                    "date": "2024-07-01",
                    "output_format": "csv",
                    "operating_unit_id": False,
                }
            )
