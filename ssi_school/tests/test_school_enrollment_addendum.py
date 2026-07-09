# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentAddendum(YamlTransactionCase):
    def test_enrollment_addendum(self):
        self.run_yaml_scenario("test_data_enrollment_addendum.yaml")

    def _create_locked_term(self):
        account_type = self.env.ref("account.data_account_type_revenue")
        account = self.env["account.account"].create(
            {
                "name": "School Fee Income ADDENPY",
                "code": "ADDENPY4200",
                "user_type_id": account_type.id,
            }
        )
        product = self.env["product.product"].create(
            {
                "name": "School Fee ADDENPY",
                "type": "service",
                "list_price": 1000000.0,
            }
        )
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type ADDENPY", "code": "GTADDENPY", "sequence": 10}
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "2024/2025 ADDENPY",
                "code": "AYADDENPY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Semester ADDENPY",
                "code": "SMADDENPY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
                "year_id": academic_year.id,
                "enrollment_state": "open",
            }
        )
        school = self.env["school"].create(
            {
                "name": "School ADDENPY",
                "code": "SCHADDENPY",
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade ADDENPY",
                "code": "GADDENPY",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class ADDENPY",
                "code": "CLAADDENPY",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = self.env["res.partner"].create({"name": "Student Contact ADDENPY"})
        student = self.env["school_student"].create(
            {
                "name": "Student ADDENPY",
                "code": "STUADDENPY",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        enrollment = self.env["school_enrollment"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
                "pricelist_id": False,
                "currency_id": self.env.company.currency_id.id,
                "receivable_journal_id": journal.id,
            }
        )
        term = self.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": enrollment.id,
                "name": "Term 1 ADDENPY",
                "sequence": 10,
            }
        )
        detail = self.env["school_enrollment_payment_term_detail"].create(
            {
                "term_id": term.id,
                "product_id": product.id,
                "name": "Fee ADDENPY",
                "account_id": account.id,
                "uom_quantity": 1.0,
                "uom_id": self.env.ref("uom.product_uom_unit").id,
                "price_unit": 1000000.0,
            }
        )
        admin = self.env.ref("base.user_admin")
        enrollment.with_user(admin).action_confirm()
        enrollment.invalidate_cache()
        enrollment.with_user(admin).action_approve_approval()
        self.assertEqual(enrollment.state, "open")
        term.invalidate_cache()
        detail.invalidate_cache()
        self.assertTrue(term.locked)
        self.assertTrue(detail.locked)
        return enrollment, term, detail

    def test_write_locked_term_raises_user_error(self):
        _enrollment, term, _detail = self._create_locked_term()
        with self.assertRaises(UserError):
            term.write({"name": "Changed Name"})

    def test_unlink_locked_term_raises_user_error(self):
        _enrollment, term, _detail = self._create_locked_term()
        with self.assertRaises(UserError):
            term.unlink()

    def test_write_locked_detail_raises_user_error(self):
        _enrollment, _term, detail = self._create_locked_term()
        with self.assertRaises(UserError):
            detail.write({"price_unit": 500000.0})

    def test_unlink_locked_detail_raises_user_error(self):
        _enrollment, _term, detail = self._create_locked_term()
        with self.assertRaises(UserError):
            detail.unlink()

    def test_close_addendum_locks_only_unlocked_terms(self):
        enrollment, term, detail = self._create_locked_term()
        admin = self.env.ref("base.user_admin")
        addendum_term = self.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": enrollment.id,
                "name": "Addendum Term ADDENPY",
                "sequence": 20,
            }
        )
        self.assertFalse(addendum_term.locked)
        enrollment.with_user(admin).action_close_addendum()
        addendum_term.invalidate_cache()
        self.assertTrue(addendum_term.locked)
        self.assertEqual(enrollment.state, "open")
        with self.assertRaises(UserError):
            addendum_term.write({"name": "Changed Name"})
        # already-locked records from before this close are unaffected
        self.assertTrue(term.locked)
        self.assertTrue(detail.locked)

    def test_addendum_can_happen_multiple_times(self):
        enrollment, _term, _detail = self._create_locked_term()
        admin = self.env.ref("base.user_admin")
        first_round = self.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": enrollment.id,
                "name": "Addendum Round 1 ADDENPY",
                "sequence": 20,
            }
        )
        enrollment.with_user(admin).action_close_addendum()
        first_round.invalidate_cache()
        self.assertTrue(first_round.locked)

        second_round = self.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": enrollment.id,
                "name": "Addendum Round 2 ADDENPY",
                "sequence": 30,
            }
        )
        self.assertFalse(second_round.locked)
        enrollment.with_user(admin).action_close_addendum()
        second_round.invalidate_cache()
        self.assertTrue(second_round.locked)
        with self.assertRaises(UserError):
            second_round.write({"name": "Changed Name"})
