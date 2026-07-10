# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentWithdrawal(YamlTransactionCase):
    def test_school_student_withdrawal(self):
        self.run_yaml_scenario("test_data_school_student_withdrawal.yaml")

    def _setup_open_enrollment(self, suffix):
        """Create grade type/school/grade/grade class/year/term/student
        and an enrollment already brought to open state, ready to be
        used as the base fixture for a withdrawal test."""
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type Withdrawal %s" % suffix,
                "code": "GTSW%s" % suffix,
                "sequence": 10,
            }
        )
        school = self.env["school"].create(
            {
                "name": "School Withdrawal %s" % suffix,
                "code": "SCHSW%s" % suffix,
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Withdrawal %s" % suffix,
                "code": "GSW%s" % suffix,
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class Withdrawal %s" % suffix,
                "code": "CLSW%s" % suffix,
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        year = self.env["school_academic_year"].create(
            {
                "name": "Year Withdrawal %s" % suffix,
                "code": "AYSW%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = self.env["school_academic_term"].create(
            {
                "name": "Term Withdrawal %s" % suffix,
                "code": "TMSW%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Contact Withdrawal %s" % suffix}
        )
        student = self.env["school_student"].create(
            {
                "name": "Student Withdrawal %s" % suffix,
                "code": "STUSW%s" % suffix,
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

    def test_constrain_student_not_enrolled_blocks_confirm(self):
        """Confirming a withdrawal for a student who is not in
        Enrolled/On Leave/Suspended state (e.g. already Graduate) must
        be rejected."""
        data = self._setup_open_enrollment("G1")
        data["student"].action_set_to_graduate()
        self.assertEqual(data["student"].state, "graduate")

        withdrawal = self.env["school_student_withdrawal"].create(
            {
                "date": "2024-08-01",
                "student_id": data["student"].id,
                "reason_type": "dropout",
            }
        )
        with self.assertRaises(ValidationError):
            withdrawal.write({"state": "confirm"})

    def test_constrain_single_active_withdrawal_for_same_student(self):
        """Only one draft/confirm withdrawal is allowed per student at
        a time; creating a second draft for the same student (which
        re-triggers the constraint, the same way a later confirm
        would) must be rejected."""
        data = self._setup_open_enrollment("M1")
        self.env["school_student_withdrawal"].create(
            {
                "date": "2024-08-01",
                "student_id": data["student"].id,
                "reason_type": "dropout",
            }
        )
        with self.assertRaises(ValidationError):
            self.env["school_student_withdrawal"].create(
                {
                    "date": "2024-08-01",
                    "student_id": data["student"].id,
                    "reason_type": "resignation",
                }
            )
