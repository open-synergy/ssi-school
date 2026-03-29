# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from ddt import ddt, file_data
from odoo_unittest_ddt import WorkflowScenarioMixin, resolve_record_ids

from odoo.tests import SavepointCase, tagged

from .common import CommonTestMixin


@tagged("post_install", "-at_install")
@ddt
class TestSchoolEnrollmentWorkflow(
    WorkflowScenarioMixin, CommonTestMixin, SavepointCase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "Grade Type for Enrollment Test",
                "code": "GTENR",
                "sequence": 10,
            }
        )
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "2024/2025 Enrollment Test",
                "code": "AYENR",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        # Create 2 academic terms so semester 1 is NOT last_term.
        # Policy done allows done_ok=True only when last_term=False.
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "Semester 1 Enrollment Test",
                "code": "SMENR1",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.academic_year.id,
                "enrollment_state": "open",
            }
        )
        cls.academic_term_2 = cls.env["school_academic_term"].create(
            {
                "name": "Semester 2 Enrollment Test",
                "code": "SMENR2",
                "date_start": "2025-01-01",
                "date_end": "2025-06-30",
                "year_id": cls.academic_year.id,
                "enrollment_state": "close",
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "School for Enrollment Test",
                "code": "SCHENR",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "Grade 1 for Enrollment",
                "code": "G1ENR",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "Class A Enrollment",
                "code": "CLAENR",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
            }
        )
        cls.contact = cls.env["res.partner"].create(
            {
                "name": "Student Contact Enrollment",
                "phone": "081234567890",
                "email": "enrstudent@test.com",
            }
        )
        cls.student = cls.env["school_student"].create(
            {
                "name": "Student for Enrollment",
                "code": "STUENTEST",
                "contact_id": cls.contact.id,
                "school_id": cls.school.id,
            }
        )

        cls.receivable_journal = cls.env["account.journal"].search(
            [("type", "=", "sale"), ("company_id", "=", cls.env.company.id)],
            limit=1,
        )

        uom = cls.env.ref("uom.product_uom_unit")
        cls.payment_template = cls.env["school_enrollment_payment_template"].create(
            {
                "name": "Enrollment Payment Template Test",
                "code": "ENRPMT001",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "academic_term_id": cls.academic_term.id,
                "term_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Term 1",
                            "sequence": 10,
                            "detail_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "product_id": cls.product.id,
                                        "name": "School Fee Term 1",
                                        "account_id": cls.account.id,
                                        "uom_quantity": 1.0,
                                        "uom_id": uom.id,
                                        "price_unit": 1_000_000.0,
                                    },
                                )
                            ],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Term 2",
                            "sequence": 20,
                            "detail_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "product_id": cls.product.id,
                                        "name": "School Fee Term 2",
                                        "account_id": cls.account.id,
                                        "uom_quantity": 1.0,
                                        "uom_id": uom.id,
                                        "price_unit": 500_000.0,
                                    },
                                )
                            ],
                        },
                    ),
                ],
            }
        )

    def _create_enrollment(self, attribute):
        vals = resolve_record_ids(self, attribute, exclude_keys=["user", "description"])
        vals["currency_id"] = self.env.company.currency_id.id
        return self.env["school_enrollment"].create(vals)

    @file_data("scenario_school_enrollment.yaml")
    def test_enrollment_workflow(self, attribute, workflow_steps):
        user_ref = attribute.get("user")
        if user_ref:
            self.env = self.env(user=self.env.ref(user_ref))
        record = self._create_enrollment(attribute)
        self.assertTrue(record.id)
        self.assertEqual(record.state, "draft")
        self.run_workflow_steps(
            record, workflow_steps, prefix="action_enrollment_", extra_data=attribute
        )

    def action_enrollment_confirm_no_error(self, record, data):
        record.action_confirm()
        self.assertEqual(record.state, "confirm")
        record.invalidate_cache()

    def action_enrollment_approve_no_error(self, record, data):
        self.assertTrue(record.approve_ok, "approve_ok should be True before approve")
        record.action_approve_approval()
        self.assertEqual(record.state, "open")
        record.invalidate_cache()

    def action_enrollment_compute_payment_no_error(self, record, data):
        record.action_compute_payment()
        record.invalidate_cache()
        self.assertEqual(
            len(record.payment_term_ids),
            2,
            "payment_term_ids harus memiliki 2 termin setelah compute payment",
        )

    def action_enrollment_create_invoice_no_error(self, record, data):
        for term in record.payment_term_ids:
            term.action_create_invoice()
            term.invalidate_cache()
            self.assertTrue(
                term.invoice_id,
                "Term '%s' harus memiliki invoice setelah create invoice" % term.name,
            )
            invoice = term.invoice_id
            self.assertAlmostEqual(
                invoice.amount_untaxed,
                term.amount_untaxed,
                places=2,
                msg="Nominal invoice '%s' harus sama dengan amount_untaxed payment term"
                % term.name,
            )
            term_details = {d.product_id.id: d for d in term.detail_ids}
            for inv_line in invoice.invoice_line_ids:
                detail = term_details.get(inv_line.product_id.id)
                self.assertIsNotNone(
                    detail,
                    "Produk '%s' pada invoice line tidak ditemukan di payment term detail"
                    % inv_line.product_id.display_name,
                )
                self.assertEqual(
                    inv_line.account_id,
                    detail.account_id,
                    "Akun invoice line '%s' harus sama dengan akun payment term detail"
                    % inv_line.product_id.display_name,
                )

    def action_enrollment_create_invoice_one_manual_no_error(self, record, data):
        terms = record.payment_term_ids.sorted("sequence")
        first_term = terms[0]
        first_term.action_mark_as_manual()
        first_term.invalidate_cache()
        self.assertEqual(
            first_term.state,
            "manual",
            "Term pertama harus berstatus 'manual' setelah mark as manual",
        )
        self.assertFalse(
            first_term.invoice_id,
            "Term pertama tidak boleh memiliki invoice setelah mark as manual",
        )
        for term in terms[1:]:
            term.action_create_invoice()
            term.invalidate_cache()
            self.assertTrue(
                term.invoice_id,
                "Term '%s' harus memiliki invoice setelah create invoice" % term.name,
            )
            invoice = term.invoice_id
            self.assertAlmostEqual(
                invoice.amount_untaxed,
                term.amount_untaxed,
                places=2,
                msg="Nominal invoice '%s' harus sama dengan amount_untaxed payment term"
                % term.name,
            )
            term_details = {d.product_id.id: d for d in term.detail_ids}
            for inv_line in invoice.invoice_line_ids:
                detail = term_details.get(inv_line.product_id.id)
                self.assertIsNotNone(
                    detail,
                    "Produk '%s' pada invoice line tidak ditemukan di payment term detail"
                    % inv_line.product_id.display_name,
                )
                self.assertEqual(
                    inv_line.account_id,
                    detail.account_id,
                    "Akun invoice line '%s' harus sama dengan akun payment term detail"
                    % inv_line.product_id.display_name,
                )

    def action_enrollment_done_no_error(self, record, data):
        record.action_done()
        self.assertEqual(record.state, "done")
