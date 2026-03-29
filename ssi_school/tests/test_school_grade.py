# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestSchoolGrade(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "Grade Type for Grade Test",
                "code": "GTGT",
                "sequence": 10,
            }
        )
        cls.grade_1 = cls.env["school_grade"].create(
            {
                "name": "Grade 1",
                "code": "G1",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_2 = cls.env["school_grade"].create(
            {
                "name": "Grade 2",
                "code": "G2",
                "sequence": 20,
                "type_id": cls.grade_type.id,
            }
        )

    # --- CREATE ---

    def test_create(self):
        record = self.env["school_grade"].create(
            {
                "name": "Grade 3",
                "code": "G3",
                "sequence": 30,
                "type_id": self.grade_type.id,
            }
        )
        self.assertTrue(record.id)
        self.assertEqual(record.name, "Grade 3")
        self.assertEqual(record.type_id, self.grade_type)

    # --- EDIT ---

    def test_edit_name(self):
        self.grade_1.write({"name": "Grade 1 Updated"})
        self.assertEqual(self.grade_1.name, "Grade 1 Updated")

    def test_edit_sequence(self):
        self.grade_1.write({"sequence": 15})
        self.assertEqual(self.grade_1.sequence, 15)

    # --- DELETE ---

    def test_delete(self):
        record = self.env["school_grade"].create(
            {
                "name": "Grade To Delete",
                "code": "GDEL",
                "sequence": 99,
                "type_id": self.grade_type.id,
            }
        )
        record_id = record.id
        record.unlink()
        self.assertFalse(self.env["school_grade"].browse(record_id).exists())

    # --- COMPUTE: previous_grade_id / next_grade_id ---

    def test_compute_next_previous_grade(self):
        """Setelah create dua grade berurutan, previous/next harus terisi."""
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type Sequence Test",
                "code": "GTST",
                "sequence": 100,
            }
        )
        g1 = self.env["school_grade"].create(
            {
                "name": "Seq Grade A",
                "code": "SGA",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        g2 = self.env["school_grade"].create(
            {
                "name": "Seq Grade B",
                "code": "SGB",
                "sequence": 20,
                "type_id": grade_type.id,
            }
        )
        # Refresh dari DB karena _recompute_next_previous mengubah semua record
        g1.invalidate_cache()
        g2.invalidate_cache()
        # Grade B harus memiliki previous_grade_id
        self.assertTrue(g2.previous_grade_id)
