# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionWorkflow(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``school_admission`` document workflow."""

    def test_admission_workflow(self):
        """Run the admission workflow scenario."""
        self.run_yaml_scenario("test_data_admission.yaml")

    def test_admission_onchange_payment_template(self):
        """Run the payment template onchange scenario.

        Covers both directions of ``payment_template_id``: selecting a
        template copies its receivable journal and account onto the
        admission, and clearing the template empties them again.
        """
        self.run_yaml_scenario("test_data_admission_onchange.yaml")

    def test_payment_template_form_view_groups_accounting_fields(self):
        """Pure Python — trigger P1 (L-01/L-02): view layout (the arch
        returned by ``fields_view_get``) is not a surface the
        ``odoo-yaml-test`` DSL can assert on, since ``action: call``
        discards the method's return value (L-01) and YAML assertions can
        only compare attributes of a registry record, not arch XML nodes
        (L-02).

        The accounting fields (``receivable_journal_id``,
        ``receivable_account_id``, ``customer_invoice_type_id``,
        ``auto_confirm_customer_invoice``) must live inside the
        ``accounting`` page, no longer as direct children of the header
        group (``group_1``) that holds the template identity fields.
        """
        result = self.env["school_admission_payment_template"].fields_view_get(
            view_type="form"
        )
        arch = etree.fromstring(result["arch"])
        accounting_fields = {
            "receivable_journal_id",
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
