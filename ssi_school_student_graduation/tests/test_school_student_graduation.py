# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentGraduation(YamlTransactionCase):
    def test_school_student_graduation(self):
        self.run_yaml_scenario("test_data_school_student_graduation.yaml")

    def _setup_open_enrollment(self, suffix):
        """Create grade type/school/grade/year/term/student and an
        enrollment already brought to open state (which also moves the
        student to the "enrol" state via the enrollment's post_open
        hook), ready to be used as the base fixture for a graduation
        test."""
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type Graduation %s" % suffix,
                "code": "GTSG%s" % suffix,
                "sequence": 10,
            }
        )
        school = self.env["school"].create(
            {
                "name": "School Graduation %s" % suffix,
                "code": "SCHSG%s" % suffix,
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Graduation %s" % suffix,
                "code": "GSG%s" % suffix,
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class Graduation %s" % suffix,
                "code": "CLSG%s" % suffix,
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        year = self.env["school_academic_year"].create(
            {
                "name": "Year Graduation %s" % suffix,
                "code": "AYSG%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = self.env["school_academic_term"].create(
            {
                "name": "Term Graduation %s" % suffix,
                "code": "TMSG%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Contact Graduation %s" % suffix}
        )
        student = self.env["school_student"].create(
            {
                "name": "Student Graduation %s" % suffix,
                "code": "STUSG%s" % suffix,
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
            "grade_class": grade_class,
            "year": year,
            "term": term,
            "student": student,
            "enrollment": enrollment,
        }

    def test_constrain_confirm_raises_when_student_dropped(self):
        """Confirming a graduation whose student is no longer in the
        "enrol" state (e.g. Dropped) must be rejected."""
        data = self._setup_open_enrollment("D1")
        data["student"].sudo().action_set_to_dropped()
        self.assertEqual(data["student"].state, "dropped")

        graduation = self.env["school_student_graduation"].create(
            {
                "date": "2025-06-30",
                "student_id": data["student"].id,
                "graduation_date": "2025-06-30",
            }
        )
        with self.assertRaises(ValidationError):
            graduation.with_user(self.env.ref("base.user_admin")).action_confirm()

    def test_constrain_single_active_graduation_for_same_student(self):
        """Only one draft/confirm graduation is allowed per student at
        a time."""
        data = self._setup_open_enrollment("M1")
        self.env["school_student_graduation"].create(
            {
                "date": "2025-06-30",
                "student_id": data["student"].id,
                "graduation_date": "2025-06-30",
            }
        )
        with self.assertRaises(ValidationError):
            self.env["school_student_graduation"].create(
                {
                    "date": "2025-06-30",
                    "student_id": data["student"].id,
                    "graduation_date": "2025-06-30",
                }
            )
