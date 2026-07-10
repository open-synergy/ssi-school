# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo_yaml_test import YamlTransactionCase

from odoo import fields
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolIncidentParentContact(YamlTransactionCase):
    def test_school_incident_parent_contact(self):
        self.run_yaml_scenario("test_data_school_incident_parent_contact.yaml")

    def _create_minimal_student(self, code_suffix, **student_extra_vals):
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type Parent Contact OC %s" % code_suffix,
                "code": "GTPCOC%s" % code_suffix,
            }
        )
        school = self.env["school"].create(
            {
                "name": "School Parent Contact OC %s" % code_suffix,
                "code": "SCHPCOC%s" % code_suffix,
                "grade_type_id": grade_type.id,
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Student Contact Parent Contact OC %s" % code_suffix}
        )
        student_vals = {
            "name": "Student Parent Contact OC %s" % code_suffix,
            "code": "STUPCOC%s" % code_suffix,
            "contact_id": contact.id,
            "school_id": school.id,
        }
        student_vals.update(student_extra_vals)
        return self.env["school_student"].create(student_vals)

    def test_onchange_parent_partner_id_from_incident(self):
        """Selecting incident_id on a parent contact log line fills
        parent_partner_id from the incident's Parent/Guardian Contact."""
        father = self.env["res.partner"].create({"name": "Father Parent Contact OC"})
        student = self._create_minimal_student("1", father_id=father.id)
        incident_type = self.env["school_incident_type"].create(
            {
                "name": "Parent Contact Onchange Case",
                "code": "INCTYPE-OC-PARENT-CONTACT-ONCHANGE",
            }
        )
        incident_form = Form(self.env["school_incident"])
        incident_form.date_incident = fields.Date.today()
        incident_form.student_id = student
        incident_form.incident_type_id = incident_type
        incident_form.description = "Case used to verify the contact onchange."
        incident = incident_form.save()
        self.assertEqual(incident.parent_partner_id, father)

        form = Form(self.env["school_incident_parent_contact"])
        form.incident_id = incident
        self.assertEqual(form.parent_partner_id, father)

    def test_inline_parent_contact_first_contact_and_date_sync(self):
        """Adding two parent_contact_ids rows inline via Form API flags the
        earliest one as First Contact and syncs date_first_contact and
        parent_contact_count on the incident."""
        student = self._create_minimal_student("2")
        incident_type = self.env["school_incident_type"].create(
            {
                "name": "Parent Contact Inline Case",
                "code": "INCTYPE-OC-PARENT-CONTACT-INLINE",
            }
        )

        later = datetime(2026, 7, 5, 10, 0, 0)
        earlier = datetime(2026, 7, 5, 8, 0, 0)

        form = Form(self.env["school_incident"])
        form.student_id = student
        form.incident_type_id = incident_type
        form.description = "Case used to verify inline parent contact log entries."
        with form.parent_contact_ids.new() as line:
            line.contact_datetime = later
            line.contact_method = "phone"
            line.summary = (
                "Empathy: thanked parent for their patience. "
                "Facts: shared the follow-up findings. "
                "Solution: confirmed the resolution."
            )
        with form.parent_contact_ids.new() as line:
            line.contact_datetime = earlier
            line.contact_method = "whatsapp"
            line.summary = (
                "Empathy: acknowledged parent's concern. "
                "Facts: confirmed what happened. "
                "Solution: agreed on next step."
            )
        incident = form.save()

        contacts = incident.parent_contact_ids.sorted("contact_datetime")
        self.assertEqual(len(contacts), 2)
        self.assertEqual(contacts[0].contact_datetime, earlier)
        self.assertTrue(contacts[0].is_first_contact)
        self.assertEqual(contacts[1].contact_datetime, later)
        self.assertFalse(contacts[1].is_first_contact)

        self.assertEqual(incident.parent_contact_count, 2)
        self.assertEqual(incident.date_first_contact, earlier)
