# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestSchool(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "Grade Type for School Test",
                "code": "GTST",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "Test School",
                "code": "SCH001",
                "grade_type_id": cls.grade_type.id,
            }
        )

    # --- CREATE ---

    def test_create(self):
        record = self.env["school"].create(
            {
                "name": "New School",
                "code": "SCH002",
                "grade_type_id": self.grade_type.id,
            }
        )
        self.assertTrue(record.id)
        self.assertEqual(record.name, "New School")
        self.assertEqual(record.grade_type_id, self.grade_type)

    # --- EDIT ---

    def test_edit_name(self):
        self.school.write({"name": "Updated School Name"})
        self.assertEqual(self.school.name, "Updated School Name")

    def test_edit_grade_type(self):
        new_grade_type = self.env["school_grade_type"].create(
            {
                "name": "Another Grade Type",
                "code": "AGT",
                "sequence": 20,
            }
        )
        self.school.write({"grade_type_id": new_grade_type.id})
        self.assertEqual(self.school.grade_type_id, new_grade_type)

    # --- DELETE ---

    def test_delete(self):
        record = self.env["school"].create(
            {
                "name": "School To Delete",
                "code": "SCHDEL",
                "grade_type_id": self.grade_type.id,
            }
        )
        record_id = record.id
        record.unlink()
        self.assertFalse(self.env["school"].browse(record_id).exists())
