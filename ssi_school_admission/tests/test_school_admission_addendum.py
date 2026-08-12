# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionAddendum(YamlTransactionCase):
    """Cover the addendum lock of admission payment terms."""

    def test_admission_addendum(self):
        """Run the admission addendum scenario."""
        self.run_yaml_scenario("test_data_admission_addendum.yaml")

    def _create_locked_term(self):
        """Build an opened admission whose term and detail are locked.

        Creates the full fixture chain (account, product, grade type,
        academic year/term, school, grade, student, admission, payment
        term and detail), then confirms and approves the admission so
        the post-open hook locks the payment plan.

        :return: tuple of the admission, its term, and its detail
        """
        account_type = self.env.ref("account.data_account_type_revenue")
        account = self.env["account.account"].create(
            {
                "name": "Admission Fee Income ADDENPY",
                "code": "ADADDENPY4200",
                "user_type_id": account_type.id,
            }
        )
        product = self.env["product.product"].create(
            {
                "name": "Admission Fee ADDENPY",
                "type": "service",
                "list_price": 2000000.0,
            }
        )
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type ADADDENPY", "code": "GTADADDENPY", "sequence": 10}
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "2024/2025 ADADDENPY",
                "code": "AYADADDENPY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Semester ADADDENPY",
                "code": "SMADADDENPY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
                "year_id": academic_year.id,
                "enrollment_state": "open",
            }
        )
        school = self.env["school"].create(
            {
                "name": "School ADADDENPY",
                "code": "SCHADADDENPY",
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade ADADDENPY",
                "code": "GADADDENPY",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        student_contact = self.env["res.partner"].create(
            {"name": "Student Contact ADADDENPY"}
        )
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        admission = self.env["school_admission"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "student_id": student_contact.id,
                "pricelist_id": False,
                "currency_id": self.env.company.currency_id.id,
                "receivable_journal_id": journal.id,
            }
        )
        term = self.env["school_admission_payment_term"].create(
            {
                "admission_id": admission.id,
                "name": "Admission Term 1 ADDENPY",
                "sequence": 10,
            }
        )
        detail = self.env["school_admission_payment_term_detail"].create(
            {
                "term_id": term.id,
                "product_id": product.id,
                "name": "Admission Fee ADDENPY",
                "account_id": account.id,
                "uom_quantity": 1.0,
                "uom_id": self.env.ref("uom.product_uom_unit").id,
                "price_unit": 2000000.0,
            }
        )
        admin = self.env.ref("base.user_admin")
        admission.with_user(admin).action_confirm()
        admission.invalidate_cache()
        admission.with_user(admin).action_approve_approval()
        self.assertEqual(admission.state, "open")
        term.invalidate_cache()
        detail.invalidate_cache()
        self.assertTrue(term.locked)
        self.assertTrue(detail.locked)
        return admission, term, detail

    def test_write_locked_term_raises_user_error(self):
        """Writing on a locked payment term is rejected.

        Pure Python -- trigger P10 (L-09/L-11): the fixture has to open
        the admission through the workflow before the assertion, which
        the ``EVAL:`` whitelist cannot express.
        """
        _admission, term, _detail = self._create_locked_term()
        with self.assertRaises(UserError):
            term.write({"name": "Changed Name"})

    def test_unlink_locked_term_raises_user_error(self):
        """Deleting a locked payment term is rejected.

        Pure Python -- trigger P10 (L-09/L-11), same fixture as
        ``test_write_locked_term_raises_user_error``.
        """
        _admission, term, _detail = self._create_locked_term()
        with self.assertRaises(UserError):
            term.unlink()

    def test_write_locked_detail_raises_user_error(self):
        """Writing on a locked term detail is rejected.

        Pure Python -- trigger P10 (L-09/L-11), same fixture as
        ``test_write_locked_term_raises_user_error``.
        """
        _admission, _term, detail = self._create_locked_term()
        with self.assertRaises(UserError):
            detail.write({"price_unit": 500000.0})

    def test_unlink_locked_detail_raises_user_error(self):
        """Deleting a locked term detail is rejected.

        Pure Python -- trigger P10 (L-09/L-11), same fixture as
        ``test_write_locked_term_raises_user_error``.
        """
        _admission, _term, detail = self._create_locked_term()
        with self.assertRaises(UserError):
            detail.unlink()

    def test_close_addendum_locks_only_unlocked_terms(self):
        """Closing an addendum locks the newly added term only.

        Terms locked by an earlier round keep their state, and the
        admission stays open.

        Pure Python -- trigger P10 (L-09/L-11): the fixture drives the
        admission through its workflow before asserting.
        """
        admission, term, detail = self._create_locked_term()
        admin = self.env.ref("base.user_admin")
        addendum_term = self.env["school_admission_payment_term"].create(
            {
                "admission_id": admission.id,
                "name": "Addendum Term ADDENPY",
                "sequence": 20,
            }
        )
        self.assertFalse(addendum_term.locked)
        admission.with_user(admin).action_close_addendum()
        addendum_term.invalidate_cache()
        self.assertTrue(addendum_term.locked)
        self.assertEqual(admission.state, "open")
        with self.assertRaises(UserError):
            addendum_term.write({"name": "Changed Name"})
        # already-locked records from before this close are unaffected
        self.assertTrue(term.locked)
        self.assertTrue(detail.locked)

    def test_addendum_can_happen_multiple_times(self):
        """Several addendum rounds may be opened and closed in turn.

        Pure Python -- trigger P10 (L-09/L-11): the fixture drives the
        admission through its workflow before asserting.
        """
        admission, _term, _detail = self._create_locked_term()
        admin = self.env.ref("base.user_admin")
        first_round = self.env["school_admission_payment_term"].create(
            {
                "admission_id": admission.id,
                "name": "Addendum Round 1 ADDENPY",
                "sequence": 20,
            }
        )
        admission.with_user(admin).action_close_addendum()
        first_round.invalidate_cache()
        self.assertTrue(first_round.locked)

        second_round = self.env["school_admission_payment_term"].create(
            {
                "admission_id": admission.id,
                "name": "Addendum Round 2 ADDENPY",
                "sequence": 30,
            }
        )
        self.assertFalse(second_round.locked)
        admission.with_user(admin).action_close_addendum()
        second_round.invalidate_cache()
        self.assertTrue(second_round.locked)
        with self.assertRaises(UserError):
            second_round.write({"name": "Changed Name"})
