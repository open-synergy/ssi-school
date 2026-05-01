# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentTemplate(YamlTransactionCase):
    def test_enrollment_payment_template(self):
        self.run_yaml_scenario("test_data_enrollment_payment_template.yaml")

    def test_onchange_school_id_clears_grade(self):
        """Mengganti school_id harus mengosongkan grade_id."""
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type PMT OC", "code": "GTPMTOC", "sequence": 10}
        )
        school = self.env["school"].create(
            {
                "name": "School PMT OC",
                "code": "SCHPMTOC",
                "grade_type_id": grade_type.id,
            }
        )
        new_school = self.env["school"].create(
            {
                "name": "Another School PMT OC",
                "code": "SCHAS3",
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade PMT OC",
                "code": "GPMTOC",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        form = Form(self.env["school_enrollment_payment_template"])
        form.name = "Onchange Template"
        form.code = "PMTOC"
        form.school_id = school
        form.grade_id = grade
        form.school_id = new_school
        self.assertFalse(form.grade_id._origin)

    def test_onchange_product_fills_name(self):
        """Memilih product harus mengisi name dari product.name."""
        account_type_income = self.env.ref("account.data_account_type_revenue")
        account = self.env["account.account"].create(
            {
                "name": "Test Income Account Detail",
                "code": "TEST4101",
                "user_type_id": account_type_income.id,
            }
        )
        product = self.env["product.product"].create(
            {
                "name": "Test Fee Product OC",
                "type": "service",
                "list_price": 500_000.0,
                "property_account_income_id": account.id,
            }
        )
        template = self.env["school_enrollment_payment_template"].create(
            {"name": "Template OC", "code": "PMTOC2"}
        )
        term = self.env["school_enrollment_payment_template.term"].create(
            {"name": "Term OC", "sequence": 10, "template_id": template.id}
        )
        with Form(self.env["school_enrollment_payment_template.term.detail"]) as form:
            form.term_id = term
            form.sequence = 30
            form.product_id = product
            form.account_id = account
            form.uom_quantity = 1.0
            self.assertEqual(form.name, product.name)

    def test_onchange_product_fills_uom(self):
        """Memilih product harus mengisi uom_id dari product.uom_id."""
        account_type_income = self.env.ref("account.data_account_type_revenue")
        account = self.env["account.account"].create(
            {
                "name": "Test Income Account UOM",
                "code": "TEST4102",
                "user_type_id": account_type_income.id,
            }
        )
        product = self.env["product.product"].create(
            {
                "name": "Test Fee Product UOM",
                "type": "service",
                "list_price": 500_000.0,
                "property_account_income_id": account.id,
            }
        )
        template = self.env["school_enrollment_payment_template"].create(
            {"name": "Template UOM OC", "code": "PMTOCUOM"}
        )
        term = self.env["school_enrollment_payment_template.term"].create(
            {"name": "Term UOM OC", "sequence": 10, "template_id": template.id}
        )
        with Form(self.env["school_enrollment_payment_template.term.detail"]) as form:
            form.term_id = term
            form.sequence = 31
            form.product_id = product
            form.account_id = account
            form.uom_quantity = 1.0
            self.assertEqual(form.uom_id, product.uom_id)

    def test_onchange_product_fills_account(self):
        """Memilih product yang punya property_account_income_id harus mengisi account_id."""
        account_type_income = self.env.ref("account.data_account_type_revenue")
        account = self.env["account.account"].create(
            {
                "name": "Test Income Account ACC",
                "code": "TEST4103",
                "user_type_id": account_type_income.id,
            }
        )
        product = self.env["product.product"].create(
            {
                "name": "Test Fee Product ACC",
                "type": "service",
                "list_price": 500_000.0,
                "property_account_income_id": account.id,
            }
        )
        template = self.env["school_enrollment_payment_template"].create(
            {"name": "Template ACC OC", "code": "PMTOCACC"}
        )
        term = self.env["school_enrollment_payment_template.term"].create(
            {"name": "Term ACC OC", "sequence": 10, "template_id": template.id}
        )
        with Form(self.env["school_enrollment_payment_template.term.detail"]) as form:
            form.term_id = term
            form.sequence = 32
            form.product_id = product
            form.uom_quantity = 1.0
            self.assertEqual(form.account_id, account)
