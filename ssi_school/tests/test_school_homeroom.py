# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolHomeroom(YamlTransactionCase):
    def test_school_homeroom(self):
        self.run_yaml_scenario("test_data_school_homeroom.yaml")

    def test_onchange_capacity_from_grade_class_id(self):
        """Setting grade_class_id must fill capacity from its capacity."""
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Homeroom Onchange", "code": "GTHRO", "sequence": 10}
        )
        school = self.env["school"].create(
            {
                "name": "School Homeroom Onchange",
                "code": "SCHHRO",
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Homeroom Onchange",
                "code": "GHRO",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class Homeroom Onchange",
                "code": "CLHRO",
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 25,
            }
        )
        year = self.env["school_academic_year"].create(
            {
                "name": "Year Homeroom Onchange",
                "code": "AYHRO",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = self.env["school_academic_term"].create(
            {
                "name": "Term Homeroom Onchange",
                "code": "TMHRO",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )

        form = Form(self.env["school_homeroom"])
        form.academic_year_id = year
        form.academic_term_id = term
        form.school_id = school
        form.grade_id = grade
        form.grade_class_id = grade_class
        self.assertEqual(form.capacity, 25)
