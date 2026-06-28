# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestCrmLeadAdmission(YamlTransactionCase):
    def test_crm_lead_admission(self):
        self.run_yaml_scenario("test_data_admission_lead.yaml")

    def test_default_academic_term_auto_filled(self):
        """Wizard should auto-fill academic_term_id from the first term open for admission."""
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Default AT", "code": "GTDAT", "sequence": 10}
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "2025/2026 Default AT",
                "code": "AYDAT2526",
                "date_start": "2025-07-01",
                "date_end": "2026-06-30",
            }
        )
        term = self.env["school_academic_term"].create(
            {
                "name": "Semester Default AT",
                "code": "SMDAT",
                "date_start": "2025-07-01",
                "date_end": "2026-06-30",
                "year_id": academic_year.id,
                "is_open_admission": True,
            }
        )
        school = self.env["school"].create(
            {
                "name": "School Default AT",
                "code": "SCHDAT",
                "grade_type_id": grade_type.id,
            }
        )
        lead = self.env["crm.lead"].create(
            {
                "name": "Lead Default AT",
                "school_id": school.id,
            }
        )
        form = Form(
            self.env["crm.lead.create_admission_form"].with_context(
                default_lead_id=lead.id,
            )
        )
        self.assertEqual(
            form.academic_term_id._origin.id,
            term.id,
            "academic_term_id should be auto-filled with the first open admission term",
        )
        self.assertEqual(
            form.academic_year_id._origin.id,
            academic_year.id,
            "academic_year_id should be auto-filled from the open admission term",
        )
