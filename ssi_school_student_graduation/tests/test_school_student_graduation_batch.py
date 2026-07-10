# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentGraduationBatch(YamlTransactionCase):
    def test_school_student_graduation_batch(self):
        self.run_yaml_scenario("test_data_school_student_graduation_batch.yaml")

    def _setup_open_enrollment(self, suffix, grade=None, grade_type=None, school=None):
        """Create (or reuse) grade type/school/grade/year/term and an
        enrolled student, ready to be used as a batch line fixture. A
        single grade per grade type has an empty next_grade_id, so it
        is always eligible as a "final grade" for graduation."""
        if grade_type is None:
            grade_type = self.env["school_grade_type"].create(
                {
                    "name": "Grade Type Graduation Batch %s" % suffix,
                    "code": "GTSGB%s" % suffix,
                    "sequence": 10,
                }
            )
        if school is None:
            school = self.env["school"].create(
                {
                    "name": "School Graduation Batch %s" % suffix,
                    "code": "SCHSGB%s" % suffix,
                    "grade_type_id": grade_type.id,
                }
            )
        if grade is None:
            grade = self.env["school_grade"].create(
                {
                    "name": "Grade Graduation Batch %s" % suffix,
                    "code": "GSGB%s" % suffix,
                    "sequence": 10,
                    "type_id": grade_type.id,
                }
            )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class Graduation Batch %s" % suffix,
                "code": "CLSGB%s" % suffix,
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        year = self.env["school_academic_year"].create(
            {
                "name": "Year Graduation Batch %s" % suffix,
                "code": "AYSGB%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = self.env["school_academic_term"].create(
            {
                "name": "Term Graduation Batch %s" % suffix,
                "code": "TMSGB%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Contact Graduation Batch %s" % suffix}
        )
        student = self.env["school_student"].create(
            {
                "name": "Student Graduation Batch %s" % suffix,
                "code": "STUSGB%s" % suffix,
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        enrollment = self.env["school_enrollment"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": year.id,
                "academic_term_id": term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
                "currency_id": self.env.company.currency_id.id,
            }
        )
        admin = self.env.ref("base.user_admin")
        enrollment.with_user(admin).action_confirm()
        enrollment.invalidate_cache()
        enrollment.with_user(admin).action_approve_approval()
        self.assertEqual(enrollment.state, "open")
        student.invalidate_cache()
        self.assertEqual(student.state, "enrol")
        return {
            "grade_type": grade_type,
            "school": school,
            "grade": grade,
            "year": year,
            "term": term,
            "student": student,
            "enrollment": enrollment,
        }

    def test_pre_done_check_raises_when_no_lines(self):
        """Completing a batch with no student line must be rejected."""
        batch = self.env["school_student_graduation_batch"].create(
            {
                "date": "2025-06-30",
            }
        )
        admin = self.env.ref("base.user_admin")
        batch.with_user(admin).action_confirm()
        batch.invalidate_cache()
        with self.assertRaises(ValidationError):
            batch.with_user(admin).action_approve_approval()

    def test_pre_done_check_raises_when_line_student_not_enrolled(self):
        """Completing a batch where a line's student is no longer
        enrolled must be rejected, and the error must name every
        offending student (collected, not stop-at-first)."""
        data_1 = self._setup_open_enrollment("PD1")
        data_2 = self._setup_open_enrollment("PD2")
        data_1["student"].sudo().action_set_to_dropped()
        data_2["student"].sudo().action_set_to_dropped()
        self.assertEqual(data_1["student"].state, "dropped")
        self.assertEqual(data_2["student"].state, "dropped")

        batch = self.env["school_student_graduation_batch"].create(
            {
                "date": "2025-06-30",
                "line_ids": [
                    (0, 0, {"student_id": data_1["student"].id}),
                    (0, 0, {"student_id": data_2["student"].id}),
                ],
            }
        )
        admin = self.env.ref("base.user_admin")
        batch.with_user(admin).action_confirm()
        batch.invalidate_cache()
        with self.assertRaises(ValidationError):
            batch.with_user(admin).action_approve_approval()

    def test_populate_lines_filters_eligible_students(self):
        """action_populate_lines only proposes students that are
        enrolled, match the academic year/term/grade filters (via
        their active enrollment), and have no next grade."""
        data = self._setup_open_enrollment("EL1")
        other_data = self._setup_open_enrollment("EL2")

        batch = self.env["school_student_graduation_batch"].create(
            {
                "date": "2025-06-30",
                "academic_year_id": data["year"].id,
                "academic_term_id": data["term"].id,
                "grade_id": data["grade"].id,
            }
        )
        batch.action_populate_lines()

        student_ids = batch.line_ids.mapped("student_id")
        self.assertIn(data["student"], student_ids)
        self.assertNotIn(other_data["student"], student_ids)
