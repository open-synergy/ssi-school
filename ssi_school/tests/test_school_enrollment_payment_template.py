# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentTemplate(YamlTransactionCase):
    def test_enrollment_payment_template(self):
        self.run_yaml_scenario("test_data_enrollment_payment_template.yaml")

    def _create_customer_invoice_type(self, suffix):
        """Create the customer invoice type required by every template."""
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        receivable_type = self.env.ref("account.data_account_type_receivable")
        account = self.env["account.account"].create(
            {
                "name": "Receivable %s" % suffix,
                "code": "RCVPMT%s" % suffix,
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        return self.env["customer_invoice_type"].create(
            {
                "name": "Customer Invoice Type %s" % suffix,
                "code": "CITPMT%s" % suffix,
                "journal_id": journal.id,
                "receivable_account_id": account.id,
            }
        )

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
        self.assertFalse(form.grade_id._origin)  # pylint: disable=protected-access

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
            {
                "name": "Template OC",
                "code": "PMTOC2",
                "customer_invoice_type_id": self._create_customer_invoice_type(
                    "OC2"
                ).id,
            }
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
            {
                "name": "Template UOM OC",
                "code": "PMTOCUOM",
                "customer_invoice_type_id": self._create_customer_invoice_type(
                    "UOM"
                ).id,
            }
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
            {
                "name": "Template ACC OC",
                "code": "PMTOCACC",
                "customer_invoice_type_id": self._create_customer_invoice_type(
                    "ACC"
                ).id,
            }
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

    def test_payment_template_form_view_groups_accounting_fields(self):
        """Pure Python — trigger P1 (L-01/L-02): view layout (the arch
        returned by ``fields_view_get``) is not a surface the
        ``odoo-yaml-test`` DSL can assert on, since ``action: call``
        discards the method's return value (L-01) and YAML assertions can
        only compare attributes of a registry record, not arch XML nodes
        (L-02).

        The accounting fields (``journal_id``, ``receivable_account_id``,
        ``customer_invoice_type_id``, ``auto_confirm_customer_invoice``)
        must live inside the ``accounting`` page, no longer as direct
        children of the header group (``group_1``) that holds the
        template identity fields.
        """
        result = self.env["school_enrollment_payment_template"].fields_view_get(
            view_type="form"
        )
        arch = etree.fromstring(result["arch"])
        accounting_fields = {
            "journal_id",
            "receivable_account_id",
            "customer_invoice_type_id",
            "auto_confirm_customer_invoice",
        }

        accounting_page = arch.find(".//page[@name='accounting']")
        self.assertIsNotNone(accounting_page, "Page accounting not found in arch")
        self.assertEqual(accounting_page.get("string"), "Accounting")
        accounting_field_names = {
            field.get("name") for field in accounting_page.findall("./group/field")
        }
        for field_name in accounting_fields:
            self.assertIn(
                field_name,
                accounting_field_names,
                "Page accounting should contain field %s" % field_name,
            )

        header_group = arch.find(".//group[@name='group_1']")
        self.assertIsNotNone(header_group, "Group group_1 not found in arch")
        header_field_names = {
            field.get("name") for field in header_group.findall("./field")
        }
        self.assertFalse(
            header_field_names & accounting_fields,
            "Accounting fields leaked into header group_1: %s"
            % (header_field_names & accounting_fields),
        )
        for identity_field in ("academic_term_id", "school_id", "grade_id"):
            self.assertIn(
                identity_field,
                header_field_names,
                "Identity field %s should stay in group_1" % identity_field,
            )
        self.assertIn(
            "is_default",
            header_field_names,
            "is_default should stay in group_1",
        )
