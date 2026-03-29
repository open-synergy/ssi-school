# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestSchoolGradeType(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "Test Grade Type",
                "code": "TGT",
                "sequence": 10,
            }
        )

    # --- CREATE ---

    def test_create(self):
        record = self.env["school_grade_type"].create(
            {
                "name": "New Grade Type",
                "code": "NGT",
                "sequence": 20,
            }
        )
        self.assertTrue(record.id)
        self.assertEqual(record.name, "New Grade Type")
        self.assertEqual(record.sequence, 20)

    # --- EDIT ---

    def test_edit_name(self):
        self.grade_type.write({"name": "Updated Grade Type"})
        self.assertEqual(self.grade_type.name, "Updated Grade Type")

    def test_edit_sequence(self):
        self.grade_type.write({"sequence": 99})
        self.assertEqual(self.grade_type.sequence, 99)

    # --- DELETE ---

    def test_delete(self):
        record = self.env["school_grade_type"].create(
            {
                "name": "To Be Deleted",
                "code": "DEL",
                "sequence": 50,
            }
        )
        record_id = record.id
        record.unlink()
        self.assertFalse(self.env["school_grade_type"].browse(record_id).exists())
