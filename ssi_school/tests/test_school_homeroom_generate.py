# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import ValidationError
from odoo.tests import tagged

# The "reconcile raises on stale non-draft enrollment" scenario asserts that
# invalid state is REJECTED (ValidationError), which the odoo-yaml-test YAML
# DSL cannot express (any exception raised by a step simply fails the
# scenario). It is written as a plain Python test instead, following the
# same precedent as test_school_homeroom_integrity.py.


@tagged("post_install", "-at_install")
class TestSchoolHomeroomGenerate(YamlTransactionCase):
    def test_school_homeroom_generate(self):
        self.run_yaml_scenario("test_data_school_homeroom_generate.yaml")

    def test_generate_raises_when_non_draft_enrollment_not_in_candidates(self):
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Homeroom Generate 5", "code": "GTHG5", "sequence": 10}
        )
        school = self.env["school"].create(
            {
                "name": "School Homeroom Generate 5",
                "code": "SCHHG5",
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade 1 Homeroom Generate 5",
                "code": "G1HG5",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class A Homeroom Generate 5",
                "code": "CLAHG5",
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 5,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "2024/2025 Homeroom Generate 5",
                "code": "AYHG5",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Semester 1 Homeroom Generate 5",
                "code": "SMHG5",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": academic_year.id,
                "enrollment_state": "open",
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Contact Homeroom Generate 5"}
        )
        student = self.env["school_student"].create(
            {
                "name": "Student Homeroom Generate 5",
                "code": "STUHG5",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        homeroom = self.env["school_homeroom"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "capacity": 5,
                "candidate_student_ids": [(6, 0, [student.id])],
            }
        )
        admin = self.env.ref("base.user_admin")
        homeroom.with_user(admin).action_confirm()
        homeroom.invalidate_cache()
        homeroom.with_user(admin).action_approve_approval()
        homeroom.with_context(queue_job__no_delay=True).action_generate_enrollments()

        enrollment = self.env["school_enrollment"].search(
            [("homeroom_id", "=", homeroom.id), ("student_id", "=", student.id)]
        )
        self.assertEqual(len(enrollment), 1)
        enrollment.with_user(admin).action_confirm()
        enrollment.invalidate_cache()
        enrollment.with_user(admin).action_approve_approval()
        self.assertEqual(enrollment.state, "open")

        homeroom.write({"candidate_student_ids": [(6, 0, [])]})
        with self.assertRaises(ValidationError):
            homeroom.action_generate_enrollments()
