# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentTemplate(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "Grade Type for Payment Template Test",
                "code": "GTPMT",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "School for Payment Template Test",
                "code": "SCHPMT",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "Grade for Payment Template Test",
                "code": "GPMT",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "2024/2025 Payment Template",
                "code": "AYPT",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "Semester 1 Payment Template",
                "code": "SMPT",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.academic_year.id,
            }
        )
        # Buat akun income untuk digunakan di template detail
        cls.account_type_income = cls.env.ref("account.data_account_type_revenue")
        cls.account = cls.env["account.account"].create(
            {
                "name": "Test Income Account",
                "code": "TEST4100",
                "user_type_id": cls.account_type_income.id,
            }
        )
        # Buat produk untuk digunakan di template detail
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test School Fee",
                "type": "service",
                "list_price": 1_000_000.0,
            }
        )
        cls.uom = cls.env.ref("uom.product_uom_unit")
        cls.template = cls.env["school_enrollment_payment_template"].create(
            {
                "name": "Payment Template Test",
                "code": "PMT001",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "academic_term_id": cls.academic_term.id,
            }
        )

    # --- CREATE ---

    def test_create(self):
        record = self.env["school_enrollment_payment_template"].create(
            {
                "name": "New Payment Template",
                "code": "PMT002",
                "school_id": self.school.id,
                "grade_id": self.grade.id,
            }
        )
        self.assertTrue(record.id)
        self.assertEqual(record.name, "New Payment Template")
        self.assertEqual(record.school_id, self.school)
        self.assertEqual(record.grade_id, self.grade)

    def test_create_without_school_and_grade(self):
        """Template boleh dibuat tanpa school/grade (not required)."""
        record = self.env["school_enrollment_payment_template"].create(
            {
                "name": "Generic Payment Template",
                "code": "PMT003",
            }
        )
        self.assertTrue(record.id)
        self.assertFalse(record.school_id)
        self.assertFalse(record.grade_id)

    def test_create_with_terms(self):
        """Template dapat dibuat sekaligus dengan term lines."""
        record = self.env["school_enrollment_payment_template"].create(
            {
                "name": "Template With Terms",
                "code": "PMTWT",
                "school_id": self.school.id,
                "term_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Term 1",
                            "sequence": 10,
                        },
                    )
                ],
            }
        )
        self.assertTrue(record.id)
        self.assertEqual(len(record.term_ids), 1)
        self.assertEqual(record.term_ids[0].name, "Term 1")

    # --- EDIT ---

    def test_edit_name(self):
        self.template.write({"name": "Updated Payment Template"})
        self.assertEqual(self.template.name, "Updated Payment Template")

    def test_edit_academic_term(self):
        new_term = self.env["school_academic_term"].create(
            {
                "name": "Semester 2 Payment Template",
                "code": "SM2PT",
                "date_start": "2025-01-01",
                "date_end": "2025-06-30",
                "year_id": self.academic_year.id,
            }
        )
        self.template.write({"academic_term_id": new_term.id})
        self.assertEqual(self.template.academic_term_id, new_term)

    def test_edit_add_term_line(self):
        """Menambahkan baris term ke template yang sudah ada."""
        self.template.write(
            {
                "term_ids": [(0, 0, {"name": "Added Term", "sequence": 20})],
            }
        )
        term = self.template.term_ids.filtered(lambda t: t.name == "Added Term")
        self.assertTrue(term)

    # --- DELETE ---

    def test_delete(self):
        record = self.env["school_enrollment_payment_template"].create(
            {
                "name": "Template To Delete",
                "code": "PMTDEL",
            }
        )
        record_id = record.id
        record.unlink()
        self.assertFalse(
            self.env["school_enrollment_payment_template"].browse(record_id).exists()
        )

    def test_delete_cascades_terms(self):
        """Menghapus template harus menghapus semua term terkait (cascade)."""
        record = self.env["school_enrollment_payment_template"].create(
            {
                "name": "Template Cascade Delete",
                "code": "PMTCSC",
                "term_ids": [(0, 0, {"name": "Cascade Term", "sequence": 10})],
            }
        )
        term_id = record.term_ids[0].id
        record.unlink()
        self.assertFalse(
            self.env["school_enrollment_payment_template.term"].browse(term_id).exists()
        )

    # --- COMPUTE: grade_type_id (related dari school) ---

    def test_compute_grade_type_from_school(self):
        """grade_type_id harus terisi otomatis dari school_id.grade_type_id."""
        record = self.env["school_enrollment_payment_template"].create(
            {
                "name": "Template Grade Type Compute",
                "code": "PMTGTC",
                "school_id": self.school.id,
            }
        )
        self.assertEqual(record.grade_type_id, self.grade_type)

    def test_compute_grade_type_empty_when_no_school(self):
        """grade_type_id harus False jika school_id tidak diisi."""
        record = self.env["school_enrollment_payment_template"].create(
            {
                "name": "Template No School",
                "code": "PMTNS",
            }
        )
        self.assertFalse(record.grade_type_id)

    # --- ONCHANGE: school_id mengosongkan grade_id ---

    def test_onchange_school_id_clears_grade(self):
        """Mengganti school_id harus mengosongkan grade_id."""
        new_school = self.env["school"].create(
            {
                "name": "Another School for PMT Onchange",
                "code": "SCHAS3",
                "grade_type_id": self.grade_type.id,
            }
        )
        form = Form(self.env["school_enrollment_payment_template"])
        form.name = "Onchange Template"
        form.code = "PMTOC"
        form.school_id = self.school
        form.grade_id = self.grade
        # Ganti school — grade_id harus dikosongkan oleh onchange
        form.school_id = new_school
        self.assertFalse(form.grade_id._origin)


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentTemplateTerm(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env["school_enrollment_payment_template"].create(
            {
                "name": "Template for Term Test",
                "code": "PMTTRM",
            }
        )
        cls.term = cls.env["school_enrollment_payment_template.term"].create(
            {
                "name": "Term A",
                "sequence": 10,
                "template_id": cls.template.id,
            }
        )

    # --- CREATE ---

    def test_create_term(self):
        record = self.env["school_enrollment_payment_template.term"].create(
            {
                "name": "Term B",
                "sequence": 20,
                "template_id": self.template.id,
            }
        )
        self.assertTrue(record.id)
        self.assertEqual(record.name, "Term B")
        self.assertEqual(record.template_id, self.template)

    # --- EDIT ---

    def test_edit_term_name(self):
        self.term.write({"name": "Term A Updated"})
        self.assertEqual(self.term.name, "Term A Updated")

    def test_edit_term_sequence(self):
        self.term.write({"sequence": 99})
        self.assertEqual(self.term.sequence, 99)

    # --- DELETE ---

    def test_delete_term(self):
        record = self.env["school_enrollment_payment_template.term"].create(
            {
                "name": "Term To Delete",
                "sequence": 50,
                "template_id": self.template.id,
            }
        )
        record_id = record.id
        record.unlink()
        self.assertFalse(
            self.env["school_enrollment_payment_template.term"]
            .browse(record_id)
            .exists()
        )


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentTemplateTermDetail(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env["school_enrollment_payment_template"].create(
            {
                "name": "Template for Detail Test",
                "code": "PMTDET",
            }
        )
        cls.term = cls.env["school_enrollment_payment_template.term"].create(
            {
                "name": "Term for Detail Test",
                "sequence": 10,
                "template_id": cls.template.id,
            }
        )
        cls.account_type_income = cls.env.ref("account.data_account_type_revenue")
        cls.account = cls.env["account.account"].create(
            {
                "name": "Test Income Account Detail",
                "code": "TEST4101",
                "user_type_id": cls.account_type_income.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Fee Product",
                "type": "service",
                "list_price": 500_000.0,
                "property_account_income_id": cls.account.id,
            }
        )
        cls.uom = cls.env.ref("uom.product_uom_unit")
        cls.detail = cls.env["school_enrollment_payment_template.term.detail"].create(
            {
                "term_id": cls.term.id,
                "sequence": 10,
                "product_id": cls.product.id,
                "name": "School Fee",
                "account_id": cls.account.id,
                "uom_quantity": 1.0,
                "uom_id": cls.uom.id,
                "price_unit": 500_000.0,
            }
        )

    # --- CREATE ---

    def test_create_detail(self):
        product = self.env["product.product"].create(
            {
                "name": "Another Fee Product",
                "type": "service",
                "list_price": 200_000.0,
            }
        )
        record = self.env["school_enrollment_payment_template.term.detail"].create(
            {
                "term_id": self.term.id,
                "sequence": 20,
                "product_id": product.id,
                "name": "Registration Fee",
                "account_id": self.account.id,
                "uom_quantity": 1.0,
                "price_unit": 200_000.0,
            }
        )
        self.assertTrue(record.id)
        self.assertEqual(record.name, "Registration Fee")
        self.assertAlmostEqual(record.price_unit, 200_000.0, places=2)

    # --- EDIT ---

    def test_edit_detail_name(self):
        self.detail.write({"name": "Updated Fee Name"})
        self.assertEqual(self.detail.name, "Updated Fee Name")

    def test_edit_detail_price(self):
        self.detail.write({"price_unit": 750_000.0})
        self.assertAlmostEqual(self.detail.price_unit, 750_000.0, places=2)

    def test_edit_detail_quantity(self):
        self.detail.write({"uom_quantity": 2.0})
        self.assertAlmostEqual(self.detail.uom_quantity, 2.0, places=2)

    # --- DELETE ---

    def test_delete_detail(self):
        product = self.env["product.product"].create(
            {
                "name": "Fee To Delete",
                "type": "service",
            }
        )
        record = self.env["school_enrollment_payment_template.term.detail"].create(
            {
                "term_id": self.term.id,
                "sequence": 99,
                "product_id": product.id,
                "name": "Fee To Delete",
                "account_id": self.account.id,
                "uom_quantity": 1.0,
                "price_unit": 100_000.0,
            }
        )
        record_id = record.id
        record.unlink()
        self.assertFalse(
            self.env["school_enrollment_payment_template.term.detail"]
            .browse(record_id)
            .exists()
        )

    # --- ONCHANGE: product_id mengisi name dan account_id ---

    def test_onchange_product_fills_name(self):
        """Memilih product harus mengisi name dari product.name."""
        with Form(self.env["school_enrollment_payment_template.term.detail"]) as form:
            form.term_id = self.term
            form.sequence = 30
            form.product_id = self.product
            form.account_id = self.account
            form.uom_quantity = 1.0
            self.assertEqual(form.name, self.product.name)

    def test_onchange_product_fills_uom(self):
        """Memilih product harus mengisi uom_id dari product.uom_id."""
        with Form(self.env["school_enrollment_payment_template.term.detail"]) as form:
            form.term_id = self.term
            form.sequence = 31
            form.product_id = self.product
            form.account_id = self.account
            form.uom_quantity = 1.0
            self.assertEqual(form.uom_id, self.product.uom_id)

    def test_onchange_product_fills_account(self):
        """Memilih product yang punya property_account_income_id harus mengisi account_id."""
        with Form(self.env["school_enrollment_payment_template.term.detail"]) as form:
            form.term_id = self.term
            form.sequence = 32
            form.product_id = self.product
            form.uom_quantity = 1.0
            self.assertEqual(form.account_id, self.account)
