# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestSchoolGradeClass(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "Grade Type for Class Test",
                "code": "GTCT",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "School for Class Test",
                "code": "SCHCT",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "Grade for Class Test",
                "code": "GCT",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "Class A",
                "code": "CA",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
            }
        )

    # --- CREATE ---

    def test_create(self):
        record = self.env["school_grade_class"].create(
            {
                "name": "Class B",
                "code": "CB",
                "school_id": self.school.id,
                "grade_id": self.grade.id,
            }
        )
        self.assertTrue(record.id)
        self.assertEqual(record.name, "Class B")
        self.assertEqual(record.school_id, self.school)
        self.assertEqual(record.grade_id, self.grade)

    # --- EDIT ---

    def test_edit_name(self):
        self.grade_class.write({"name": "Class A Updated"})
        self.assertEqual(self.grade_class.name, "Class A Updated")

    def test_edit_grade(self):
        new_grade = self.env["school_grade"].create(
            {
                "name": "Grade 2 for Class",
                "code": "G2C",
                "sequence": 20,
                "type_id": self.grade_type.id,
            }
        )
        self.grade_class.write({"grade_id": new_grade.id})
        self.assertEqual(self.grade_class.grade_id, new_grade)

    # --- DELETE ---

    def test_delete(self):
        record = self.env["school_grade_class"].create(
            {
                "name": "Class To Delete",
                "code": "CDEL",
                "school_id": self.school.id,
                "grade_id": self.grade.id,
            }
        )
        record_id = record.id
        record.unlink()
        self.assertFalse(self.env["school_grade_class"].browse(record_id).exists())

    # --- COMPUTE: grade_type_id (related dari school) ---

    def test_compute_grade_type_from_school(self):
        """grade_type_id harus terisi otomatis dari school_id."""
        record = self.env["school_grade_class"].create(
            {
                "name": "Class Compute Test",
                "code": "CCT",
                "school_id": self.school.id,
                "grade_id": self.grade.id,
            }
        )
        self.assertEqual(record.grade_type_id, self.grade_type)

    # --- ONCHANGE: school_id mengosongkan grade_id ---

    def test_onchange_school_id_clears_grade(self):
        """Mengganti school_id harus mengosongkan grade_id."""
        new_school = self.env["school"].create(
            {
                "name": "Another School",
                "code": "SCHAS",
                "grade_type_id": self.grade_type.id,
            }
        )
        form = Form(self.env["school_grade_class"])
        form.name = "Onchange Test Class"
        form.code = "OTC"
        form.school_id = self.school
        form.grade_id = self.grade
        # Ganti school — grade_id harus dikosongkan oleh onchange
        form.school_id = new_school
        self.assertFalse(form.grade_id._origin)
