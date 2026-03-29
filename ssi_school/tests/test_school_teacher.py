# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestSchoolTeacher(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.contact = cls.env["res.partner"].create(
            {
                "name": "Teacher Contact",
                "phone": "081234567890",
                "email": "teacher@test.com",
            }
        )
        cls.teacher = cls.env["school_teacher"].create(
            {
                "name": "Teacher 1",
                "code": "TCH001",
                "contact_id": cls.contact.id,
            }
        )

    # --- CREATE ---

    def test_create(self):
        contact = self.env["res.partner"].create({"name": "New Teacher Contact"})
        record = self.env["school_teacher"].create(
            {
                "name": "New Teacher",
                "code": "TCH002",
                "contact_id": contact.id,
            }
        )
        self.assertTrue(record.id)
        self.assertEqual(record.name, "New Teacher")
        self.assertEqual(record.contact_id, contact)

    # --- EDIT ---

    def test_edit_name(self):
        self.teacher.write({"name": "Teacher 1 Updated"})
        self.assertEqual(self.teacher.name, "Teacher 1 Updated")

    def test_edit_contact(self):
        new_contact = self.env["res.partner"].create(
            {"name": "Another Teacher Contact"}
        )
        self.teacher.write({"contact_id": new_contact.id})
        self.assertEqual(self.teacher.contact_id, new_contact)

    # --- DELETE ---

    def test_delete(self):
        contact = self.env["res.partner"].create({"name": "Teacher To Delete Contact"})
        record = self.env["school_teacher"].create(
            {
                "name": "Teacher To Delete",
                "code": "TCHDEL",
                "contact_id": contact.id,
            }
        )
        record_id = record.id
        record.unlink()
        self.assertFalse(self.env["school_teacher"].browse(record_id).exists())

    # --- COMPUTE: field related dari contact ---

    def test_related_phone_from_contact(self):
        """phone harus terisi dari contact_id.phone."""
        self.assertEqual(self.teacher.phone, self.contact.phone)

    def test_related_email_from_contact(self):
        """email harus terisi dari contact_id.email."""
        self.assertEqual(self.teacher.email, self.contact.email)
