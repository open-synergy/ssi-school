# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolEnrollmentPaymentTemplate(HttpSavepointCase):
    """Tour tests for the ``school_enrollment_payment_template`` IK."""

    @classmethod
    def setUpClass(cls):
        """Prepare the product, invoice types, records, and print data."""
        super().setUpClass()
        # Pre-Condition IK is prepared here -- NOT by clicking through
        # the UI. ``school_enrollment_payment_template_group`` already
        # includes ``base.user_admin`` (security/res_group_data.xml), so
        # no extra group grant is required for the menu to be visible.
        #
        # Pre-Condition for docs/school_enrollment_payment_template/
        # 01-create.md: a product with an income account, picked from
        # the many2one dropdown for the fee detail line -- onchange_name
        # and onchange_account_id
        # (school_enrollment_payment_template_term_detail.py) fill Name
        # and Account from it automatically.
        cls.account_income = cls.env["account.account"].create(
            {
                "name": "TOUR PMT Income Account",
                "code": "TOURPMTINC",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "TOUR PMT PRODUCT",
                "type": "service",
                "list_price": 500_000.0,
                "property_account_income_id": cls.account_income.id,
            }
        )

        cls.customer_invoice_type_create = cls._create_customer_invoice_type("CREATE")
        cls.template_edit = cls.env["school_enrollment_payment_template"].create(
            {
                "name": "TOUR PMT EDIT",
                "code": "/",
                "customer_invoice_type_id": cls._create_customer_invoice_type(
                    "EDIT"
                ).id,
            }
        )
        cls.template_delete = cls.env["school_enrollment_payment_template"].create(
            {
                "name": "TOUR PMT DELETE",
                "code": "TOURPMTDEL",
                "customer_invoice_type_id": cls._create_customer_invoice_type(
                    "DELETE"
                ).id,
            }
        )
        cls.template_deactivate = cls.env["school_enrollment_payment_template"].create(
            {
                "name": "TOUR PMT DEACTIVATE",
                "code": "TOURPMTDEA",
                "customer_invoice_type_id": cls._create_customer_invoice_type(
                    "DEACTIVATE"
                ).id,
            }
        )
        cls.template_activate = cls.env["school_enrollment_payment_template"].create(
            {
                "name": "TOUR PMT ACTIVATE",
                "code": "TOURPMTACT",
                "customer_invoice_type_id": cls._create_customer_invoice_type(
                    "ACTIVATE"
                ).id,
                "active": False,
            }
        )

        # Pre-Condition for Generate Code
        # (docs/school_enrollment_payment_template/01-create.md and
        # 02-edit.md): an active ``sequence.template`` for this model is
        # required, or clicking the button raises a UserError instead of
        # assigning a code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Payment Template Code Sequence",
                "code": "ssi_school.tour.school_enrollment_payment_template",
                "prefix": "TOURSEQPMT",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Payment Template Sequence Template",
                "model_id": cls.env["ir.model"]._get_id(
                    "school_enrollment_payment_template"
                ),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("school_enrollment_payment_template", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("school_enrollment_payment_template", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        # Pre-Condition for the print tour
        # (docs/school_enrollment_payment_template/06-print.md): a
        # ``print_document_type`` linking a report to
        # ``school_enrollment_payment_template`` is required for the
        # wizard to have a report to offer -- without it the wizard
        # still opens but the report list is empty. The tour itself
        # never selects nor prints the report (see test_print
        # docstring), so the report action is a placeholder that is
        # never rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Payment Template Report",
                "model": "school_enrollment_payment_template",
                "report_type": "qweb-pdf",
                "report_name": (
                    "ssi_school.tour_school_enrollment_payment_template_report"
                ),
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Payment Template Print Type",
                "model_id": cls.env["ir.model"]._get_id(
                    "school_enrollment_payment_template"
                ),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.template_print = cls.env["school_enrollment_payment_template"].create(
            {
                "name": "TOUR PMT PRINT",
                "code": "TOURPMTPRN",
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
                "name": "TOUR PMT Receivable %s" % suffix,
                "code": "TOURPMTRCV%s" % suffix,
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        return cls.env["customer_invoice_type"].create(
            {
                "name": "TOUR PMT INVOICE TYPE %s" % suffix,
                "code": "TOURCITPMT%s" % suffix,
                "journal_id": journal.id,
                "receivable_account_id": account.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_enrollment_payment_template``.

        IK: docs/school_enrollment_payment_template/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_enrollment_payment_template_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_enrollment_payment_template``.

        IK: docs/school_enrollment_payment_template/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_enrollment_payment_template_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_enrollment_payment_template``.

        IK: docs/school_enrollment_payment_template/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_enrollment_payment_template_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for the payment template model.

        IK: docs/school_enrollment_payment_template/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_enrollment_payment_template_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for the payment template model.

        IK: docs/school_enrollment_payment_template/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_enrollment_payment_template_activate",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_enrollment_payment_template/06-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour(
            "/web",
            "ssi_school_school_enrollment_payment_template_print",
            login="admin",
        )
