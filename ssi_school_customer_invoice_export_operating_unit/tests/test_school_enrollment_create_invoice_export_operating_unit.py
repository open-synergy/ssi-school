# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentCreateInvoiceExportOperatingUnit(YamlTransactionCase):
    """Cover the Operating Unit selection on the Create Invoice Export
    wizard for school enrollments.

    Exercises the YAML behavior scenarios (default value, filtering by
    operating unit, mismatched operating unit) and the Python-only
    required-field scenario below.
    """

    def test_school_enrollment_create_invoice_export_operating_unit(self):
        """Run the operating unit selection scenarios."""
        self.run_yaml_scenario(
            "test_data_school_enrollment_create_invoice_export_operating_unit.yaml"
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
        this test deliberately triggers.
        """
        enrollment_model = self.env["school_enrollment"]
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type ROU1", "code": "GTROU1", "sequence": 10}
        )
        school = self.env["school"].create(
            {"name": "School ROU1", "code": "SCHROU1", "grade_type_id": grade_type.id}
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade ROU1",
                "code": "GROU1",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class ROU1",
                "code": "CLROU1",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "2024/2025 ROU1",
                "code": "AYROU1",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Semester ROU1",
                "code": "SMROU1",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
                "year_id": academic_year.id,
                "enrollment_state": "open",
            }
        )
        contact = self.env["res.partner"].create({"name": "Student Contact ROU1"})
        student = self.env["school_student"].create(
            {
                "name": "Student ROU1",
                "code": "STUROU1",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        enrollment = enrollment_model.create(
            {
                "date": "2024-07-01",
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
            }
        )
        export_type = self.env["customer_invoice_export_type"].create(
            {
                "name": "Export Type ROU1",
                "code": "ETYROU1",
                "default_output_format": "csv",
            }
        )
        # type_id/date/output_format are filled in so the NOT NULL
        # violation below can only come from operating_unit_id, not
        # from one of the base wizard's own required fields.
        with self.assertRaises(IntegrityError):
            self.env["school_enrollment.wizard_create_invoice_export"].create(
                {
                    "enrollment_ids": [(6, 0, enrollment.ids)],
                    "type_id": export_type.id,
                    "date": "2024-07-01",
                    "output_format": "csv",
                    "operating_unit_id": False,
                }
            )
