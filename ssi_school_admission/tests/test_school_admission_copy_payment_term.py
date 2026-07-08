# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionCopyPaymentTerm(YamlTransactionCase):
    def test_admission_copy_payment_term(self):
        self.run_yaml_scenario("test_data_admission_copy_payment_term.yaml")

    def _create_base_data(self, suffix):
        account_type = self.env.ref("account.data_account_type_revenue")
        account = self.env["account.account"].create(
            {
                "name": "Admission Fee Income %s" % suffix,
                "code": "ACPTRBLK%s4200" % suffix,
                "user_type_id": account_type.id,
            }
        )
        product = self.env["product.product"].create(
            {
                "name": "Admission Fee %s" % suffix,
                "type": "service",
                "list_price": 500000.0,
            }
        )
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type %s" % suffix,
                "code": "GT%s" % suffix,
                "sequence": 10,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "2024/2025 %s" % suffix,
                "code": "AY%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Semester %s" % suffix,
                "code": "SM%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
                "year_id": academic_year.id,
                "enrollment_state": "open",
            }
        )
        school = self.env["school"].create(
            {
                "name": "School %s" % suffix,
                "code": "SCH%s" % suffix,
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade %s" % suffix,
                "code": "G%s" % suffix,
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        return {
            "account": account,
            "product": product,
            "academic_year": academic_year,
            "academic_term": academic_term,
            "school": school,
            "grade": grade,
        }

    def _create_admission(self, base, name_suffix, grade=None):
        contact = self.env["res.partner"].create(
            {"name": "Student Contact %s" % name_suffix}
        )
        return self.env["school_admission"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": base["academic_year"].id,
                "academic_term_id": base["academic_term"].id,
                "school_id": base["school"].id,
                "grade_id": (grade or base["grade"]).id,
                "student_id": contact.id,
                "currency_id": self.env.company.currency_id.id,
            }
        )

    def _create_source_term(self, base, source):
        term = self.env["school_admission_payment_term"].create(
            {
                "admission_id": source.id,
                "name": "Term Source %s" % source.id,
                "sequence": 10,
            }
        )
        self.env["school_admission_payment_term_detail"].create(
            {
                "term_id": term.id,
                "product_id": base["product"].id,
                "name": "Fee %s" % source.id,
                "account_id": base["account"].id,
                "uom_quantity": 1.0,
                "uom_id": self.env.ref("uom.product_uom_unit").id,
                "price_unit": 500000.0,
            }
        )
        return term

    def test_copy_payment_term_blocked_when_target_not_draft(self):
        base = self._create_base_data("BLK1")
        source = self._create_admission(base, "BLK1SRC")
        self._create_source_term(base, source)
        target = self._create_admission(base, "BLK1TGT")
        target.write({"state": "confirm"})

        wizard = (
            self.env["school_admission.wizard_copy_payment_term"]
            .with_context(active_model="school_admission", active_ids=target.ids)
            .create(
                {
                    "source_admission_id": source.id,
                    "mode": "replace",
                }
            )
        )
        self.assertEqual(wizard.target_admission_ids, target)
        self.assertFalse(target.copy_payment_term_ok)

        with self.assertRaises(UserError):
            wizard.action_copy_payment_term()

        self.assertFalse(target.payment_term_ids)

    def test_copy_payment_term_blocked_when_grade_mismatch(self):
        base = self._create_base_data("BLK2")
        source = self._create_admission(base, "BLK2SRC")
        self._create_source_term(base, source)

        other_grade = self.env["school_grade"].create(
            {
                "name": "Other Grade BLK2",
                "code": "OGBLK2",
                "sequence": 20,
                "type_id": base["grade"].type_id.id,
            }
        )
        target = self._create_admission(base, "BLK2TGT", grade=other_grade)

        wizard = (
            self.env["school_admission.wizard_copy_payment_term"]
            .with_context(active_model="school_admission", active_ids=target.ids)
            .create(
                {
                    "source_admission_id": source.id,
                    "mode": "replace",
                }
            )
        )
        self.assertTrue(target.copy_payment_term_ok)

        with self.assertRaises(UserError):
            wizard.action_copy_payment_term()

        self.assertFalse(target.payment_term_ids)
