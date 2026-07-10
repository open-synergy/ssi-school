# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolStudent(YamlTransactionCase):
    def test_student(self):
        self.run_yaml_scenario("test_data_student.yaml")

    def _create_school(self, code):
        grade_type = self.env["school_grade_type"].create(
            {
                "name": f"Grade Type Dup Constrain {code}",
                "code": f"GTDC{code}",
                "sequence": 10,
            }
        )
        return self.env["school"].create(
            {
                "name": f"School Dup Constrain {code}",
                "code": f"SCHDC{code}",
                "grade_type_id": grade_type.id,
            }
        )

    def _create_student(self, code, school, name=None):
        contact = self.env["res.partner"].create(
            {"name": name or f"Dup Constrain Contact {code}"}
        )
        return self.env["school_student"].create(
            {
                "name": name or f"Dup Constrain Student {code}",
                "code": code,
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )

    def test_duplicate_code_same_school_raises(self):
        """Two students sharing a code within the same school must fail."""
        school = self._create_school("DUP02")
        self._create_student("DUP02", school)
        with self.assertRaises(UserError):
            self._create_student("DUP02", school)

    def test_move_student_to_school_causing_duplicate_raises(self):
        """Moving a student into a school where its code already exists
        must trigger the constraint, since it re-checks on school_id change."""
        school_a = self._create_school("MOVA")
        school_b = self._create_school("MOVB")
        self._create_student("MOVDUP", school_b)
        student_a = self._create_student("MOVDUP", school_a)
        with self.assertRaises(UserError):
            student_a.write({"school_id": school_b.id})

    def test_onchange_school_id_clears_initial_grade(self):
        """Mengganti school_id harus mengosongkan initial_grade_id."""
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Student OC", "code": "GTSOC", "sequence": 10}
        )
        school = self.env["school"].create(
            {
                "name": "School Student OC",
                "code": "SCHSOC",
                "grade_type_id": grade_type.id,
            }
        )
        new_school = self.env["school"].create(
            {
                "name": "Another School Student OC",
                "code": "SCHASOC",
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Student OC",
                "code": "GSOC",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        contact = self.env["res.partner"].create({"name": "Onchange Student Contact"})
        form = Form(self.env["school_student"])
        form.name = "Onchange Student"
        form.code = "STUOC"
        form.contact_id = contact
        form.school_id = school
        form.initial_grade_id = grade
        form.school_id = new_school
        self.assertFalse(
            form.initial_grade_id._origin  # pylint: disable=protected-access
        )
