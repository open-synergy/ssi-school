# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentWorkflow(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "Grade Type for Enrollment Test",
                "code": "GTENR",
                "sequence": 10,
            }
        )
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "2024/2025 Enrollment Test",
                "code": "AYENR",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        # Create 2 academic terms so semester 1 is NOT last_term.
        # Policy done allows done_ok=True only when last_term=False.
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "Semester 1 Enrollment Test",
                "code": "SMENR1",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.academic_year.id,
                "enrollment_state": "open",
            }
        )
        cls.academic_term_2 = cls.env["school_academic_term"].create(
            {
                "name": "Semester 2 Enrollment Test",
                "code": "SMENR2",
                "date_start": "2025-01-01",
                "date_end": "2025-06-30",
                "year_id": cls.academic_year.id,
                "enrollment_state": "close",
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "School for Enrollment Test",
                "code": "SCHENR",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "Grade 1 for Enrollment",
                "code": "G1ENR",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "Class A Enrollment",
                "code": "CLAENR",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
            }
        )
        cls.contact = cls.env["res.partner"].create(
            {
                "name": "Student Contact Enrollment",
                "phone": "081234567890",
                "email": "enrstudent@test.com",
            }
        )
        cls.student = cls.env["school_student"].create(
            {
                "name": "Student for Enrollment",
                "code": "STUENTEST",
                "contact_id": cls.contact.id,
                "school_id": cls.school.id,
            }
        )

    def _create_enrollment(self):
        return self.env["school_enrollment"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": self.academic_year.id,
                "academic_term_id": self.academic_term.id,
                "school_id": self.school.id,
                "grade_id": self.grade.id,
                "grade_class_id": self.grade_class.id,
                "student_id": self.student.id,
                "currency_id": self.env.company.currency_id.id,
            }
        )

    def test_create_then_confirm(self):
        record = self._create_enrollment()
        self.assertTrue(record.id)
        self.assertEqual(record.state, "draft")
        record.action_confirm()
        self.assertEqual(record.state, "confirm")

    def test_create_confirm_approve_done(self):
        # Run as user_admin (uid=2) who is in school_enrollment_validator_group.
        # The approve_ok policy checks env.user.id in active_approver_user_ids,
        # and active_approver_user_ids is derived from group.users which excludes
        # uid=1 (OdooBot/user_root — internal system user).
        self.env = self.env(user=self.env.ref("base.user_admin"))
        record = self._create_enrollment()
        self.assertTrue(record.id)
        self.assertEqual(record.state, "draft")

        record.action_confirm()
        self.assertEqual(record.state, "confirm")
        # Invalidate record cache so approval_ids (One2many) is re-read from DB.
        record.invalidate_cache()

        self.assertTrue(record.approve_ok, "approve_ok should be True after confirm")

        record.action_approve_approval()
        self.assertEqual(record.state, "open")
        record.invalidate_cache()

        record.action_done()
        self.assertEqual(record.state, "done")
