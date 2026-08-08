# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.tests import HttpSavepointCase, tagged

_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install")
class TestUiSchoolEnrollmentCreateInvoiceExport(HttpSavepointCase):
    """Tour test for the Create Invoice Export wizard on enrollment."""

    @classmethod
    def setUpClass(cls):
        """Build an Open enrollment with one unpaid invoiced term.

        ``SavepointCase.setUpClass`` runs ``cls.env`` as SUPERUSER_ID, so
        any fixture created via ``cls.env.create()`` without an explicit
        ``user_id`` defaults "Responsible" to the superuser, not
        "admin" -- ``school_enrollment_internal_user_rule`` (scoped by
        ``user_id``) would then hide it from the "admin" tour session.
        ``user_id`` is set explicitly below (mirrors
        ``test_ui_school_admission.py``).

        Builds the accounting basics (journal/account/customer invoice
        type/income account/product), the academic structure (grade
        type, academic year/term, school, grade, grade class), one
        student, one On Progress enrollment (advanced past its policy
        gates via ``bypass_policy_check``, mirroring
        ``test_ui_school_enrollment.py``), one active Customer Invoice
        Export Type (Pre-Condition Data), and one payment term whose
        generated invoice is confirmed and approved to Unpaid (open) --
        the Pre-Condition this IK's wizard needs before its button
        becomes visible (``create_invoice_export_ok``).
        """
        super().setUpClass()
        cls.admin_user = cls.env.ref("base.user_admin")

        # -- Accounting basics -------------------------------------------
        cls.ci_journal = cls.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        receivable_type = cls.env.ref("account.data_account_type_receivable")
        cls.ci_account = cls.env["account.account"].create(
            {
                "name": "TOUR ENR IE Receivable",
                "code": "TOURENRIERCV",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        cls.ci_type = cls.env["customer_invoice_type"].create(
            {
                "name": "TOUR ENR IE CI Type",
                "code": "TOURENRIECIT",
                "journal_id": cls.ci_journal.id,
                "receivable_account_id": cls.ci_account.id,
            }
        )
        income_type = cls.env.ref("account.data_account_type_revenue")
        cls.income_account = cls.env["account.account"].create(
            {
                "name": "TOUR ENR IE Income",
                "code": "TOURENRIEINC",
                "user_type_id": income_type.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "TOUR ENR IE Fee",
                "type": "service",
                "list_price": 1_000_000.0,
            }
        )

        # -- Academic structure -------------------------------------------
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR ENR IE Grade Type", "code": "TOURENRIEGT"}
        )
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ENR IE Academic Year",
                "code": "TOURENRIEAY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR ENR IE Term",
                "code": "TOURENRIET",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
                "year_id": cls.academic_year.id,
                "enrollment_state": "open",
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR ENR IE School",
                "code": "TOURENRIESCH",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "TOUR ENR IE Grade",
                "code": "TOURENRIEG",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR ENR IE Class",
                "code": "TOURENRIECL",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
            }
        )

        # -- Student --------------------------------------------------------
        contact = cls.env["res.partner"].create({"name": "TOUR ENR IE Student"})
        cls.student = cls.env["school_student"].create(
            {
                "name": "TOUR ENR IE Student",
                "code": "/",
                "school_id": cls.school.id,
                "contact_id": contact.id,
            }
        )

        # -- Export type (23-create-invoice-export.md Pre-Condition Data) -
        cls.export_type = cls.env["customer_invoice_export_type"].create(
            {
                "name": "TOUR ENR IE Export Type",
                "code": "TOURENRIEET",
                "default_output_format": "csv",
            }
        )

        # -- Policy: grant create_invoice_export_ok (23-create-invoice-
        # export.md Pre-Condition Config) -----------------------------
        # The shipped policy_template_school_enrollment already ships a
        # policy.template_detail for this field
        # (policy_template/school_enrollment.xml), but its correctness
        # cannot be assumed from the test side -- write/create it
        # explicitly here too (mirrors
        # test_ui_school_enrollment.py's restart_approval_ok setup) so
        # this tour's Pre-Condition is guaranteed regardless of the
        # shipped data. computation_method "use_group" is evaluated
        # against the REAL browsing user ("admin", not the superuser
        # cls.env runs as during setUpClass), so the group is also
        # granted to admin explicitly below.
        state_field = cls.env["ir.model.fields"].search(
            [("model_id.model", "=", "school_enrollment"), ("name", "=", "state")],
            limit=1,
        )
        open_done_selections = cls.env["ir.model.fields.selection"].search(
            [
                ("field_id", "=", state_field.id),
                ("value", "in", ["open", "done"]),
            ]
        )
        create_invoice_export_field = cls.env["ir.model.fields"].search(
            [
                ("model_id.model", "=", "school_enrollment"),
                ("name", "=", "create_invoice_export_ok"),
            ],
            limit=1,
        )
        enrollment_user_group = cls.env.ref("ssi_school.school_enrollment_user_group")
        policy_detail_vals = {
            "restrict_state": True,
            "state_ids": [(6, 0, open_done_selections.ids)],
            "restrict_user": True,
            "computation_method": "use_group",
            "group_ids": [(6, 0, [enrollment_user_group.id])],
            "restrict_additional": False,
        }
        existing_detail = cls.env["policy.template_detail"].search(
            [
                (
                    "template_id",
                    "=",
                    cls.env.ref("ssi_school.policy_template_school_enrollment").id,
                ),
                ("field_id", "=", create_invoice_export_field.id),
            ],
            limit=1,
        )
        if existing_detail:
            existing_detail.write(policy_detail_vals)
        else:
            policy_detail_vals.update(
                {
                    "template_id": cls.env.ref(
                        "ssi_school.policy_template_school_enrollment"
                    ).id,
                    "field_id": create_invoice_export_field.id,
                }
            )
            cls.env["policy.template_detail"].create(policy_detail_vals)
        enrollment_user_group.sudo().write({"users": [(4, cls.admin_user.id)]})

        # -- Enrollment, advanced to Open (On Progress) ---------------------
        cls.enrollment = cls.env["school_enrollment"].create(
            {
                "user_id": cls.admin_user.id,
                "customer_invoice_type_id": cls.ci_type.id,
                "receivable_account_id": cls.ci_account.id,
                "pricelist_id": cls.env.ref("product.list0").id,
                "date": "2024-07-01",
                "academic_year_id": cls.academic_year.id,
                "academic_term_id": cls.academic_term.id,
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "grade_class_id": cls.grade_class.id,
                "student_id": cls.student.id,
                "currency_id": cls.env.company.currency_id.id,
                "receivable_journal_id": cls.ci_journal.id,
            }
        )
        cls.enrollment.with_context(bypass_policy_check=True).action_confirm()
        cls.enrollment.invalidate_cache()
        _logger.info(
            "DIAG-ENR after confirm: state=%s template=%s approvals=%s",
            cls.enrollment.state,
            cls.enrollment.approval_template_id.display_name,
            [
                (a.status, a.approver_user_ids.ids, a.approver_selection_method)
                for a in cls.enrollment.approval_ids
            ],
        )
        cls.enrollment.with_context(bypass_policy_check=True).action_approve_approval()
        cls.enrollment.invalidate_cache()
        _logger.info(
            "DIAG-ENR after approve: state=%s approvals=%s env_uid=%s",
            cls.enrollment.state,
            [(a.status, a.approver_user_ids.ids) for a in cls.enrollment.approval_ids],
            cls.env.uid,
        )

        # -- Payment term with an Unpaid (open) invoiced move ---------------
        cls.term_open = cls.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": cls.enrollment.id,
                "name": "TOUR ENR IE Open Term",
                "sequence": 10,
                "detail_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "name": "TOUR ENR IE Open Fee",
                            "account_id": cls.income_account.id,
                            "uom_quantity": 1.0,
                            "uom_id": cls.env.ref("uom.product_uom_unit").id,
                            "price_unit": 1_000_000.0,
                        },
                    )
                ],
            }
        )
        cls.term_open.action_create_invoice()
        cls.invoice_open = cls.term_open.customer_invoice_id
        cls.invoice_open.with_context(bypass_policy_check=True).action_confirm()
        cls.invoice_open.invalidate_cache()
        cls.invoice_open.with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        cls.invoice_open.invalidate_cache()

    def test_create_invoice_export(self):
        """Run the create-invoice-export tour on the Open enrollment.

        IK: docs/school_enrollment/23-create-invoice-export.md
        """
        self.start_tour(
            "/web",
            "ssi_school_customer_invoice_export_school_enrollment_create_invoice_export",
            login="admin",
        )
