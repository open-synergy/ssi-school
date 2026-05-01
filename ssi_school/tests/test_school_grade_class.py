# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolGradeClass(YamlTransactionCase):
    def test_grade_class(self):
        self.run_yaml_scenario("test_data_grade_class.yaml")

    def test_onchange_school_id_clears_grade(self):
        """Mengganti school_id harus mengosongkan grade_id."""
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Onchange", "code": "GTOC", "sequence": 10}
        )
        school = self.env["school"].create(
            {"name": "School Onchange", "code": "SCHOC", "grade_type_id": grade_type.id}
        )
        new_school = self.env["school"].create(
            {"name": "Another School", "code": "SCHAS", "grade_type_id": grade_type.id}
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Onchange",
                "code": "GOC",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        form = Form(self.env["school_grade_class"])
        form.name = "Onchange Test Class"
        form.code = "OTC"
        form.school_id = school
        form.grade_id = grade
        form.school_id = new_school
        self.assertFalse(form.grade_id._origin)
