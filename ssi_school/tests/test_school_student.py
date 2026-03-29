# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestSchoolStudent(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "Grade Type for Student Test",
                "code": "GTSTU",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "School for Student Test",
                "code": "SCHSTU",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "Grade 1 for Student",
                "code": "G1STU",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.contact = cls.env["res.partner"].create(
            {
                "name": "Student Contact",
                "phone": "081111111111",
                "email": "student@test.com",
            }
        )
        cls.student = cls.env["school_student"].create(
            {
                "name": "Student 1",
                "code": "STU001",
                "contact_id": cls.contact.id,
                "school_id": cls.school.id,
            }
        )

    # --- CREATE ---

    def test_create(self):
        contact = self.env["res.partner"].create({"name": "New Student Contact"})
        record = self.env["school_student"].create(
            {
                "name": "New Student",
                "code": "STU002",
                "contact_id": contact.id,
                "school_id": self.school.id,
            }
        )
        self.assertTrue(record.id)
        self.assertEqual(record.name, "New Student")
        self.assertEqual(record.school_id, self.school)
        self.assertEqual(record.state, "draft")

    # --- EDIT ---

    def test_edit_name(self):
        self.student.write({"name": "Student 1 Updated"})
        self.assertEqual(self.student.name, "Student 1 Updated")

    def test_edit_school(self):
        new_school = self.env["school"].create(
            {
                "name": "New School for Student",
                "code": "SCHNEW",
                "grade_type_id": self.grade_type.id,
            }
        )
        self.student.write({"school_id": new_school.id})
        self.assertEqual(self.student.school_id, new_school)

    # --- DELETE ---

    def test_delete(self):
        contact = self.env["res.partner"].create({"name": "Student To Delete Contact"})
        record = self.env["school_student"].create(
            {
                "name": "Student To Delete",
                "code": "STUDEL",
                "contact_id": contact.id,
                "school_id": self.school.id,
            }
        )
        record_id = record.id
        record.unlink()
        self.assertFalse(self.env["school_student"].browse(record_id).exists())

    # --- COMPUTE: initial_grade_type_id (related dari school) ---

    def test_compute_initial_grade_type_from_school(self):
        """initial_grade_type_id harus terisi dari school_id.grade_type_id."""
        student = self.env["school_student"].create(
            {
                "name": "Student Compute Test",
                "code": "STUCT",
                "contact_id": self.contact.id,
                "school_id": self.school.id,
            }
        )
        self.assertEqual(student.initial_grade_type_id, self.grade_type)

    def test_compute_current_grade_no_enrollment(self):
        """Tanpa enrollment, current_grade_id = initial_grade_id."""
        student = self.env["school_student"].create(
            {
                "name": "Student No Enrollment",
                "code": "STUNE",
                "contact_id": self.contact.id,
                "school_id": self.school.id,
                "initial_grade_id": self.grade.id,
            }
        )
        student.invalidate_cache()
        self.assertEqual(student.current_grade_id, self.grade)

    def test_compute_active_enrollment_none(self):
        """Tanpa enrollment aktif, active_enrollment_id harus False."""
        student = self.env["school_student"].create(
            {
                "name": "Student No Active Enrol",
                "code": "STUNAE",
                "contact_id": self.contact.id,
                "school_id": self.school.id,
            }
        )
        self.assertFalse(student.active_enrollment_id)

    # --- ONCHANGE: school_id mengosongkan initial_grade_id ---

    def test_onchange_school_id_clears_initial_grade(self):
        """Mengganti school_id harus mengosongkan initial_grade_id."""
        new_school = self.env["school"].create(
            {
                "name": "Another School for Onchange",
                "code": "SCHAS2",
                "grade_type_id": self.grade_type.id,
            }
        )
        contact = self.env["res.partner"].create({"name": "Onchange Student Contact"})
        form = Form(self.env["school_student"])
        form.name = "Onchange Student"
        form.code = "STUOC"
        form.contact_id = contact
        form.school_id = self.school
        form.initial_grade_id = self.grade
        # Ganti school — initial_grade_id harus dikosongkan
        form.school_id = new_school
        self.assertFalse(form.initial_grade_id._origin)

    # --- ACTION METHODS (tombol di view) ---

    def test_action_set_to_enroll(self):
        """Tombol Enroll: draft → enrol."""
        student = self.env["school_student"].create(
            {
                "name": "Student For Enroll Action",
                "code": "STUENR",
                "contact_id": self.contact.id,
                "school_id": self.school.id,
            }
        )
        self.assertEqual(student.state, "draft")
        student.action_set_to_enroll()
        self.assertEqual(student.state, "enrol")

    def test_action_set_to_draft(self):
        """Tombol Reset to Draft: enrol → draft."""
        student = self.env["school_student"].create(
            {
                "name": "Student For Draft Action",
                "code": "STUDRT",
                "contact_id": self.contact.id,
                "school_id": self.school.id,
            }
        )
        student.action_set_to_enroll()
        student.action_set_to_draft()
        self.assertEqual(student.state, "draft")

    def test_action_set_to_on_leave(self):
        """Tombol On Leave: → on_leave."""
        student = self.env["school_student"].create(
            {
                "name": "Student For On Leave Action",
                "code": "STUOL",
                "contact_id": self.contact.id,
                "school_id": self.school.id,
            }
        )
        student.action_set_to_on_leave()
        self.assertEqual(student.state, "on_leave")

    def test_action_set_to_suspended(self):
        """Tombol Suspended: → suspended."""
        student = self.env["school_student"].create(
            {
                "name": "Student For Suspended Action",
                "code": "STUSP",
                "contact_id": self.contact.id,
                "school_id": self.school.id,
            }
        )
        student.action_set_to_suspended()
        self.assertEqual(student.state, "suspended")

    def test_action_set_to_graduate(self):
        """Tombol Graduate: → graduate."""
        student = self.env["school_student"].create(
            {
                "name": "Student For Graduate Action",
                "code": "STUGR",
                "contact_id": self.contact.id,
                "school_id": self.school.id,
            }
        )
        student.action_set_to_graduate()
        self.assertEqual(student.state, "graduate")

    def test_action_set_to_transferred(self):
        """Tombol Transferred: → transferred."""
        student = self.env["school_student"].create(
            {
                "name": "Student For Transferred Action",
                "code": "STUTR",
                "contact_id": self.contact.id,
                "school_id": self.school.id,
            }
        )
        student.action_set_to_transferred()
        self.assertEqual(student.state, "transferred")

    def test_action_set_to_dropped(self):
        """Tombol Dropped: → dropped."""
        student = self.env["school_student"].create(
            {
                "name": "Student For Dropped Action",
                "code": "STUDP",
                "contact_id": self.contact.id,
                "school_id": self.school.id,
            }
        )
        student.action_set_to_dropped()
        self.assertEqual(student.state, "dropped")

    def test_action_set_to_resigned(self):
        """Tombol Resigned: → resigned."""
        student = self.env["school_student"].create(
            {
                "name": "Student For Resigned Action",
                "code": "STURS",
                "contact_id": self.contact.id,
                "school_id": self.school.id,
            }
        )
        student.action_set_to_resigned()
        self.assertEqual(student.state, "resigned")

    def test_action_set_to_deceased(self):
        """Tombol Deceased: → deceased."""
        student = self.env["school_student"].create(
            {
                "name": "Student For Deceased Action",
                "code": "STUDC",
                "contact_id": self.contact.id,
                "school_id": self.school.id,
            }
        )
        student.action_set_to_deceased()
        self.assertEqual(student.state, "deceased")
