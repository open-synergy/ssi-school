# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolAdmissionFeeTemplate(HttpCase):
    """UI/UX tour tests for ``school_admission_fee_template``.

    Every ``test_*`` method runs the tour pairing with the IK file named
    in its docstring (``docs/school_admission_fee_template/NN-*.md``).
    Pre-Condition data is prepared here in Python, never through UI
    steps.
    """

    @classmethod
    def setUpClass(cls):
        """Create the product/account and one fixture per tour."""
        super().setUpClass()

        income_type = cls.env.ref("account.data_account_type_revenue")
        cls.income_account = cls.env["account.account"].create(
            {
                "name": "TOUR ADM FEE TPL INCOME",
                "code": "TOURADMFTI",
                "user_type_id": income_type.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {"name": "TOUR ADM FEE TPL PRODUCT"}
        )

        # Generate Code (01-create.md / 02-edit.md) requires an active
        # sequence.template for this model.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Admission Fee Template Code Sequence",
                "code": "ssi_school_admission.tour.school_admission_fee_template",
                "prefix": "TOURSEQAFT",
                "padding": 4,
            }
        )
        cls.env["sequence.template"].create(
            {
                "name": "TOUR Admission Fee Template Sequence Template",
                "model_id": cls.env["ir.model"]._get_id(
                    "school_admission_fee_template"
                ),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("school_admission_fee_template", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("school_admission_fee_template", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        # 02-edit.md -- Code left as "/" so Generate Code has effect.
        cls.template_edit = cls.env["school_admission_fee_template"].create(
            {"name": "TOUR ADM FEE TPL EDIT", "code": "/"}
        )
        # 03-delete.md
        cls.template_delete = cls.env["school_admission_fee_template"].create(
            {"name": "TOUR ADM FEE TPL DELETE", "code": "TOURADMFTDEL"}
        )
        # 04-deactivate.md
        cls.template_deactivate = cls.env["school_admission_fee_template"].create(
            {"name": "TOUR ADM FEE TPL DEACTIVATE", "code": "TOURADMFTDEA"}
        )
        # 05-activate.md
        cls.template_activate = cls.env["school_admission_fee_template"].create(
            {
                "name": "TOUR ADM FEE TPL ACTIVATE",
                "code": "TOURADMFTACT",
                "active": False,
            }
        )

        # 06-print.md -- a print_document_type linking a report to this
        # model, so the wizard has a report to offer. The tour never
        # selects nor prints it (patterns.md §Q).
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Admission Fee Template Report",
                "model": "school_admission_fee_template",
                "report_type": "qweb-pdf",
                "report_name": (
                    "ssi_school_admission.tour_school_admission_fee_template_report"
                ),
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Admission Fee Template Print Type",
                "model_id": cls.env["ir.model"]._get_id(
                    "school_admission_fee_template"
                ),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.template_print = cls.env["school_admission_fee_template"].create(
            {"name": "TOUR ADM FEE TPL PRINT", "code": "TOURADMFTPRN"}
        )

    def test_create(self):
        """IK: docs/school_admission_fee_template/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_fee_template_create",
            login="admin",
        )

    def test_edit(self):
        """IK: docs/school_admission_fee_template/02-edit.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_fee_template_edit",
            login="admin",
        )

    def test_delete(self):
        """IK: docs/school_admission_fee_template/03-delete.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_fee_template_delete",
            login="admin",
        )

    def test_deactivate(self):
        """IK: docs/school_admission_fee_template/04-deactivate.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_fee_template_deactivate",
            login="admin",
        )

    def test_activate(self):
        """IK: docs/school_admission_fee_template/05-activate.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_fee_template_activate",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_admission_fee_template/06-print.md

        Boundary: never selects a report nor clicks the wizard's own
        Print button -- the resulting report action is an
        ``ir.actions.act_url`` download with no DOM "finished" signal.
        See patterns.md §Q.
        """
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_fee_template_print",
            login="admin",
        )
