# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionTest(YamlTransactionCase):
    def test_admission_test_workflow(self):
        self.run_yaml_scenario("test_data_admission_test_workflow.yaml")

    def test_admission_form_uniqueness_constraint(
        self,
    ):  # pylint: disable=too-many-locals
        """Test that two admission tests cannot share the same admission form."""
        grade_type_model = self.env["school_grade_type"]
        academic_year_model = self.env["school_academic_year"]
        academic_term_model = self.env["school_academic_term"]
        school_model = self.env["school"]
        grade_model = self.env["school_grade"]
        partner_model = self.env["res.partner"]
        admission_form_model = self.env["school_admission_form"]
        admission_test_model = self.env["school_admission_test"]

        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        account_type = self.env.ref("account.data_account_type_revenue")
        account = self.env["account.account"].create(
            {
                "name": "Admission Fee Income Uniqueness Test",
                "code": "ADUNIQ4200",
                "user_type_id": account_type.id,
            }
        )
        pricelist = self.env["product.pricelist"].create(
            {
                "name": "Pricelist ADUNIQ",
                "currency_id": self.env.company.currency_id.id,
            }
        )

        grade_type = grade_type_model.create(
            {"name": "Grade Type Uniqueness", "code": "GTUNIQ", "sequence": 10}
        )
        academic_year = academic_year_model.create(
            {
                "name": "2024/2025 Uniqueness",
                "code": "AYUNIQ",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        academic_term = academic_term_model.create(
            {
                "name": "Semester Uniqueness",
                "code": "SMUNIQ",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
                "year_id": academic_year.id,
                "enrollment_state": "open",
            }
        )
        school = school_model.create(
            {
                "name": "School Uniqueness",
                "code": "SCHUNIQ",
                "grade_type_id": grade_type.id,
            }
        )
        grade = grade_model.create(
            {
                "name": "Grade Uniqueness",
                "code": "GUNIQ",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        student_contact = partner_model.create({"name": "Student Uniqueness"})
        parent_contact = partner_model.create({"name": "Parent Uniqueness"})

        admission_form = admission_form_model.create(
            {
                "date": "2024-07-01",
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "student_id": student_contact.id,
                "parent_id": parent_contact.id,
                "pricelist_id": pricelist.id,
                "currency_id": self.env.company.currency_id.id,
                "journal_id": journal.id,
                "account_id": account.id,
            }
        )

        admission_test_model.create(
            {
                "date": "2024-07-01",
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "student_id": student_contact.id,
                "admission_form_id": admission_form.id,
            }
        )

        with self.assertRaises(ValidationError):
            admission_test_model.create(
                {
                    "date": "2024-07-01",
                    "academic_year_id": academic_year.id,
                    "academic_term_id": academic_term.id,
                    "school_id": school.id,
                    "grade_id": grade.id,
                    "student_id": student_contact.id,
                    "admission_form_id": admission_form.id,
                }
            )
