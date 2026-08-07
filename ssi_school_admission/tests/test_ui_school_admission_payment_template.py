# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolAdmissionPaymentTemplate(HttpSavepointCase):
    """UI/UX tour tests for ``school_admission_payment_template``.

    Every ``test_*`` method runs the tour pairing with the IK file named
    in its docstring (``docs/school_admission_payment_template/NN-*.md``).
    """

    @classmethod
    def setUpClass(cls):
        """Create the product/account, invoice types, and fixtures."""
        super().setUpClass()

        cls.account_income = cls.env["account.account"].create(
            {
                "name": "TOUR ADM PMT TPL Income Account",
                "code": "TOURADMPTI",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "TOUR ADM PMT TPL PRODUCT",
                "type": "service",
                "list_price": 500_000.0,
                "property_account_income_id": cls.account_income.id,
            }
        )

        cls.customer_invoice_type_create = cls._create_customer_invoice_type("CREATE")
        cls.template_edit = cls.env["school_admission_payment_template"].create(
            {
                "name": "TOUR ADM PMT TPL EDIT",
                "code": "/",
                "customer_invoice_type_id": cls._create_customer_invoice_type(
                    "EDIT"
                ).id,
            }
        )
        cls.template_delete = cls.env["school_admission_payment_template"].create(
            {
                "name": "TOUR ADM PMT TPL DELETE",
                "code": "TOURADMPTDEL",
                "customer_invoice_type_id": cls._create_customer_invoice_type(
                    "DELETE"
                ).id,
            }
        )
        cls.template_deactivate = cls.env["school_admission_payment_template"].create(
            {
                "name": "TOUR ADM PMT TPL DEACTIVATE",
                "code": "TOURADMPTDEA",
                "customer_invoice_type_id": cls._create_customer_invoice_type(
                    "DEACTIVATE"
                ).id,
            }
        )
        cls.template_activate = cls.env["school_admission_payment_template"].create(
            {
                "name": "TOUR ADM PMT TPL ACTIVATE",
                "code": "TOURADMPTACT",
                "customer_invoice_type_id": cls._create_customer_invoice_type(
                    "ACTIVATE"
                ).id,
                "active": False,
            }
        )

        # Generate Code requires an active sequence.template.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Admission Payment Template Code Sequence",
                "code": "ssi_school_admission.tour.school_admission_payment_template",
                "prefix": "TOURSEQAPT",
                "padding": 4,
            }
        )
        cls.env["sequence.template"].create(
            {
                "name": "TOUR Admission Payment Template Sequence Template",
                "model_id": cls.env["ir.model"]._get_id(
                    "school_admission_payment_template"
                ),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("school_admission_payment_template", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("school_admission_payment_template", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        # 06-print.md
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Admission Payment Template Report",
                "model": "school_admission_payment_template",
                "report_type": "qweb-pdf",
                "report_name": (
                    "ssi_school_admission."
                    "tour_school_admission_payment_template_report"
                ),
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Admission Payment Template Print Type",
                "model_id": cls.env["ir.model"]._get_id(
                    "school_admission_payment_template"
                ),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.template_print = cls.env["school_admission_payment_template"].create(
            {
                "name": "TOUR ADM PMT TPL PRINT",
                "code": "TOURADMPTPRN",
                "customer_invoice_type_id": cls._create_customer_invoice_type(
                    "PRINT"
                ).id,
            }
        )

    @classmethod
    def _create_customer_invoice_type(cls, suffix):
        """Create the customer invoice type required by a template."""
        journal = cls.env["account.journal"].search([("type", "=", "sale")], limit=1)
        receivable_type = cls.env.ref("account.data_account_type_receivable")
        account = cls.env["account.account"].create(
            {
                "name": "TOUR ADM PMT TPL Receivable %s" % suffix,
                "code": "TOURAPTRCV%s" % suffix,
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        return cls.env["customer_invoice_type"].create(
            {
                "name": "TOUR ADM PMT TPL INVOICE TYPE %s" % suffix,
                "code": "TOURCITAPT%s" % suffix,
                "journal_id": journal.id,
                "receivable_account_id": account.id,
            }
        )

    def test_create(self):
        """IK: docs/school_admission_payment_template/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_payment_template_create",
            login="admin",
        )

    def test_edit(self):
        """IK: docs/school_admission_payment_template/02-edit.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_payment_template_edit",
            login="admin",
        )

    def test_delete(self):
        """IK: docs/school_admission_payment_template/03-delete.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_payment_template_delete",
            login="admin",
        )

    def test_deactivate(self):
        """IK: docs/school_admission_payment_template/04-deactivate.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_payment_template_deactivate",
            login="admin",
        )

    def test_activate(self):
        """IK: docs/school_admission_payment_template/05-activate.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_payment_template_activate",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_admission_payment_template/06-print.md
        """
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_payment_template_print",
            login="admin",
        )
