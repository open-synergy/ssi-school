# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolStudent(YamlTransactionCase):
    def test_student(self):
        self.run_yaml_scenario("test_data_student.yaml")

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
        self.assertFalse(form.initial_grade_id._origin)
