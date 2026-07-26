# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionRestartUnlock(YamlTransactionCase):
    def test_admission_restart_unlock(self):
        self.run_yaml_scenario("test_data_admission_restart_unlock.yaml")

    def _create_base_data(self, suffix):
        """Build the shared master data used by every scenario here."""
        account_type = self.env.ref("account.data_account_type_revenue")
        account = self.env["account.account"].create(
            {
                "name": "Admission Fee Income %s" % suffix,
                "code": "ADRSTUNLK%s4200" % suffix,
                "user_type_id": account_type.id,
            }
        )
        product = self.env["product.product"].create(
            {
                "name": "Admission Fee %s" % suffix,
                "type": "service",
                "list_price": 2000000.0,
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
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        receivable_type = self.env.ref("account.data_account_type_receivable")
        receivable_account = self.env["account.account"].create(
            {
                "name": "Admission Receivable %s" % suffix,
                "code": "ADRSTUNLK%s1100" % suffix,
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        customer_invoice_type = self.env["customer_invoice_type"].create(
            {
                "name": "Customer Invoice Type %s" % suffix,
                "code": "ADCIT%s" % suffix,
                "journal_id": journal.id,
                "receivable_account_id": receivable_account.id,
            }
        )
        return {
            "account": account,
            "product": product,
            "academic_year": academic_year,
            "academic_term": academic_term,
            "school": school,
            "grade": grade,
            "journal": journal,
            "receivable_account": receivable_account,
            "customer_invoice_type": customer_invoice_type,
        }

    def _create_admission(self, base, name_suffix):
        """Create an admission wired to the customer invoice fixtures."""
        student_contact = self.env["res.partner"].create(
            {"name": "Student Contact %s" % name_suffix}
        )
        return self.env["school_admission"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": base["academic_year"].id,
                "academic_term_id": base["academic_term"].id,
                "school_id": base["school"].id,
                "grade_id": base["grade"].id,
                "student_id": student_contact.id,
                "pricelist_id": self.env.ref("product.list0").id,
                "currency_id": self.env.company.currency_id.id,
                "receivable_journal_id": base["journal"].id,
                "receivable_account_id": base["receivable_account"].id,
                "customer_invoice_type_id": base["customer_invoice_type"].id,
            }
        )

    def _add_term(self, base, admission, suffix):
        term = self.env["school_admission_payment_term"].create(
            {
                "admission_id": admission.id,
                "name": "Admission Term %s" % suffix,
                "sequence": 10,
            }
        )
        detail = self.env["school_admission_payment_term_detail"].create(
            {
                "term_id": term.id,
                "product_id": base["product"].id,
                "name": "Admission Fee %s" % suffix,
                "account_id": base["account"].id,
                "uom_quantity": 1.0,
                "uom_id": self.env.ref("uom.product_uom_unit").id,
                "price_unit": 2000000.0,
            }
        )
        return term, detail

    def _open_admission(self, admission):
        admin = self.env.ref("base.user_admin")
        admission.with_user(admin).action_confirm()
        admission.invalidate_cache()
        admission.with_user(admin).action_approve_approval()
        self.assertEqual(admission.state, "open")

    def test_lock_not_leaked_without_cancel(self):
        base = self._create_base_data("NOREG1")
        admission = self._create_admission(base, "NOREG1")
        term, detail = self._add_term(base, admission, "NOREG1")
        self._open_admission(admission)
        term.invalidate_cache()
        detail.invalidate_cache()
        self.assertTrue(term.locked)
        self.assertTrue(detail.locked)
        with self.assertRaises(UserError):
            term.write({"name": "Changed Name NOREG1"})

    def test_copy_payment_term_after_restart(self):
        base = self._create_base_data("CPTRST1")
        target = self._create_admission(base, "CPTRST1TGT")
        old_term, _old_detail = self._add_term(base, target, "CPTRST1OLD")
        self._open_admission(target)

        admin = self.env.ref("base.user_admin")
        target.invalidate_cache()
        target.with_user(admin).action_cancel()
        self.assertEqual(target.state, "cancel")
        target.invalidate_cache()
        target.with_user(admin).action_restart()
        self.assertEqual(target.state, "draft")
        old_term.invalidate_cache()
        self.assertFalse(old_term.locked)

        source = self._create_admission(base, "CPTRST1SRC")
        self._add_term(base, source, "CPTRST1NEW")

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
        wizard.action_copy_payment_term()

        target.invalidate_cache()
        self.assertEqual(len(target.payment_term_ids), 1)
        self.assertEqual(target.payment_term_ids.name, "Admission Term CPTRST1NEW")

    def test_cancel_blocked_when_invoice_exists(self):
        base = self._create_base_data("CXLINV1")
        admission = self._create_admission(base, "CXLINV1")
        term, _detail = self._add_term(base, admission, "CXLINV1")
        self._open_admission(admission)

        term.action_create_invoice()
        term.invalidate_cache()
        self.assertTrue(term.customer_invoice_id)

        admission.invalidate_cache()
        self.assertFalse(admission.cancel_ok)

        admin = self.env.ref("base.user_admin")
        with self.assertRaises(UserError):
            admission.with_user(admin).action_cancel()

        term.action_delete_invoice()
        term.invalidate_cache()
        self.assertFalse(term.customer_invoice_id)

        admission.invalidate_cache()
        self.assertTrue(admission.cancel_ok)

        admission.with_user(admin).action_cancel()
        self.assertEqual(admission.state, "cancel")
