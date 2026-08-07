# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields
from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolAdmission(HttpCase):
    """UI/UX tour tests for the ``school_admission`` work instructions.

    Every ``test_*`` method runs the tour pairing with the IK file named
    in its docstring (``docs/school_admission/NN-*.md``). Fixtures are
    advanced past a policy gate with ``bypass_policy_check=True`` as
    Pre-Condition setup (mirrors ``test_ui_school_enrollment.py``).
    """

    @classmethod
    def setUpClass(cls):
        """Build the academic/school/payment structure and fixtures."""
        super().setUpClass()

        # -- Academic / school structure ---------------------------------
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ADM Academic Year",
                "code": "TOURADMAY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR ADM Term",
                "code": "TOURADMT",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.academic_year.id,
            }
        )
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR ADM Grade Type", "code": "TOURADMGT"}
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR ADM School",
                "code": "TOURADMSCH",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "TOUR ADM Grade",
                "code": "TOURADMG",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        # 16-create-enrollment.md -- required Grade Class in the wizard.
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR ADM Grade Class",
                "code": "TOURADMGC",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
            }
        )

        # -- Payment template (01-create.md / 02-edit.md) ----------------
        cls.income_account = cls.env["account.account"].create(
            {
                "name": "TOUR ADM Income",
                "code": "TOURADMINC",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )
        cls.pmt_product = cls.env["product.product"].create(
            {
                "name": "TOUR ADM PMT Product",
                "type": "service",
                "property_account_income_id": cls.income_account.id,
            }
        )
        cls.ci_journal = cls.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        cls.ci_account = cls.env["account.account"].create(
            {
                "name": "TOUR ADM Receivable",
                "code": "TOURADMRCV",
                "user_type_id": cls.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )
        cls.ci_type = cls.env["customer_invoice_type"].create(
            {
                "name": "TOUR ADM CI Type",
                "code": "TOURADMCIT",
                "journal_id": cls.ci_journal.id,
                "receivable_account_id": cls.ci_account.id,
            }
        )
        cls.payment_template = cls.env["school_admission_payment_template"].create(
            {
                "name": "TOUR ADM Payment Template",
                "code": "TOURADMPT",
                "customer_invoice_type_id": cls.ci_type.id,
                "term_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "TOUR ADM Payment Term",
                            "sequence": 10,
                            "detail_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "product_id": cls.pmt_product.id,
                                        "name": "TOUR ADM Payment Term Detail",
                                        "account_id": cls.income_account.id,
                                        "uom_quantity": 1.0,
                                        "uom_id": cls.env.ref(
                                            "uom.product_uom_unit"
                                        ).id,
                                        "price_unit": 1_000_000.0,
                                    },
                                )
                            ],
                        },
                    )
                ],
            }
        )

        # -- Policy: grant restart_approval_ok / manual_number_ok --------
        # The shipped policy_template_school_admission has NO detail for
        # either field, so they are always False out of the box. Add
        # test-only details on the SAME shipped template, mirroring the
        # blocker workaround in test_ui_school_enrollment.py.
        state_field = cls.env["ir.model.fields"].search(
            [
                ("model_id.model", "=", "school_admission"),
                ("name", "=", "state"),
            ],
            limit=1,
        )
        draft_selection = cls.env["ir.model.fields.selection"].search(
            [("field_id", "=", state_field.id), ("value", "=", "draft")],
            limit=1,
        )
        confirm_selection = cls.env["ir.model.fields.selection"].search(
            [("field_id", "=", state_field.id), ("value", "=", "confirm")],
            limit=1,
        )
        manual_number_field = cls.env["ir.model.fields"].search(
            [
                ("model_id.model", "=", "school_admission"),
                ("name", "=", "manual_number_ok"),
            ],
            limit=1,
        )
        restart_approval_field = cls.env["ir.model.fields"].search(
            [
                ("model_id.model", "=", "school_admission"),
                ("name", "=", "restart_approval_ok"),
            ],
            limit=1,
        )
        policy_template = cls.env.ref(
            "ssi_school_admission.policy_template_school_admission"
        )
        user_group = cls.env.ref("ssi_school_admission.school_admission_user_group")
        cls.env["policy.template_detail"].create(
            {
                "template_id": policy_template.id,
                "field_id": manual_number_field.id,
                "restrict_state": True,
                "state_ids": [(6, 0, draft_selection.ids)],
                "restrict_user": True,
                "computation_method": "use_group",
                "group_ids": [(6, 0, user_group.ids)],
                "restrict_additional": False,
            }
        )
        cls.env["policy.template_detail"].create(
            {
                "template_id": policy_template.id,
                "field_id": restart_approval_field.id,
                "restrict_state": True,
                "state_ids": [(6, 0, confirm_selection.ids)],
                "restrict_user": True,
                "computation_method": "use_group",
                "group_ids": [(6, 0, user_group.ids)],
                "restrict_additional": False,
            }
        )

        # -- Access: the Policies tab (19-reload-template-policy.md) is
        # only visible to base.group_system.
        cls.env.ref("base.group_system").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

        # -- Cancel reason (10-cancel.md) ---------------------------------
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR ADM Cancel Reason",
                "code": "TOUR-ADM-CANCEL",
                "global_use": True,
            }
        )

        # -- Print document type (18-print.md) -----------------------------
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Admission Report",
                "model": "school_admission",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school_admission.tour_school_admission_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Admission Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_admission"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )

        def _create_admission(student_name):
            """Create a Draft ``school_admission`` fixture."""
            student = cls.env["res.partner"].create({"name": student_name})
            return cls.env["school_admission"].create(
                {
                    "academic_year_id": cls.academic_year.id,
                    "academic_term_id": cls.academic_term.id,
                    "school_id": cls.school.id,
                    "grade_id": cls.grade.id,
                    "student_id": student.id,
                    "currency_id": cls.env.company.currency_id.id,
                }
            )

        def _bypass(record):
            """Advance a fixture past a policy gate as Pre-Condition setup."""
            return record.with_context(bypass_policy_check=True)

        # 01-create.md -- eligible Student to pick from the dropdown.
        cls.student_create = cls.env["res.partner"].create(
            {"name": "TOUR ADM Create Student"}
        )

        # 02-edit.md
        cls.admission_edit = _create_admission("TOUR ADM Edit Student")

        # 03-delete.md
        cls.admission_delete = _create_admission("TOUR ADM Delete Student")

        # 04-confirm.md
        cls.admission_confirm = _create_admission("TOUR ADM Confirm Student")

        # 05-approve.md
        cls.admission_approve = _create_admission("TOUR ADM Approve Student")
        _bypass(cls.admission_approve).action_confirm()

        # 06-reject.md
        cls.admission_reject = _create_admission("TOUR ADM Reject Student")
        _bypass(cls.admission_reject).action_confirm()

        # 09-finish.md -- On Progress record to finish.
        cls.admission_finish = _create_admission("TOUR ADM Finish Student")
        _bypass(cls.admission_finish).action_confirm()
        _bypass(cls.admission_finish).action_approve_approval()

        # 10-cancel.md
        cls.admission_cancel = _create_admission("TOUR ADM Cancel Student")

        # 12-restart.md -- Rejected record to restart.
        cls.admission_restart = _create_admission("TOUR ADM Restart Student")
        _bypass(cls.admission_restart).action_confirm()
        _bypass(cls.admission_restart).action_reject_approval()
        if cls.admission_restart.state != "reject":
            cls.admission_restart.sudo().write({"state": "reject"})

        # 13-reset-number.md
        cls.admission_reset_number = _create_admission("TOUR ADM Reset Number Student")
        cls.admission_reset_number.write({"name": "TOUR-ADM-MANUAL-001"})

        # 14-restart-approval.md
        cls.admission_restart_approval = _create_admission(
            "TOUR ADM Restart Approval Student"
        )
        _bypass(cls.admission_restart_approval).action_confirm()

        # 15-create-due-invoice.md -- On Progress, one Uninvoiced term
        # whose Date Invoice is on or before today.
        cls.admission_invoice = _create_admission("TOUR ADM Invoice Student")
        _bypass(cls.admission_invoice).action_confirm()
        _bypass(cls.admission_invoice).action_approve_approval()
        cls.env["school_admission_payment_term"].create(
            {
                "admission_id": cls.admission_invoice.id,
                "name": "TOUR ADM DUE TERM",
                "sequence": 10,
                "date_invoice": fields.Date.today() - timedelta(days=1),
            }
        )

        # 16-create-enrollment.md -- On Progress (school_student created
        # automatically by action_approve_approval).
        cls.admission_enrollment = _create_admission("TOUR ADM Enrollment Student")
        _bypass(cls.admission_enrollment).action_confirm()
        _bypass(cls.admission_enrollment).action_approve_approval()

        # 17-close-addendum.md -- On Progress, one currently UNLOCKED
        # term. Post-open locking only affects terms that existed BEFORE
        # the admission opened, so this term is added afterwards.
        cls.admission_addendum = _create_admission("TOUR ADM Addendum Student")
        _bypass(cls.admission_addendum).action_confirm()
        _bypass(cls.admission_addendum).action_approve_approval()
        cls.env["school_admission_payment_term"].create(
            {
                "admission_id": cls.admission_addendum.id,
                "name": "TOUR ADM ADDENDUM TERM",
                "sequence": 10,
            }
        )

        # 18-print.md -- any record; Print does not depend on status.
        cls.admission_print = _create_admission("TOUR ADM Print Student")

        # 19-reload-template-policy.md
        cls.admission_reload_policy = _create_admission(
            "TOUR ADM Reload Policy Student"
        )
        cls.admission_reload_policy.write({"policy_template_id": False})

    def test_create(self):
        """IK: docs/school_admission/01-create.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_create", login="admin"
        )

    def test_edit(self):
        """IK: docs/school_admission/02-edit.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_edit", login="admin"
        )

    def test_delete(self):
        """IK: docs/school_admission/03-delete.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_delete", login="admin"
        )

    def test_confirm(self):
        """IK: docs/school_admission/04-confirm.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_confirm", login="admin"
        )

    def test_approve(self):
        """IK: docs/school_admission/05-approve.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_approve", login="admin"
        )

    def test_reject(self):
        """IK: docs/school_admission/06-reject.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_reject", login="admin"
        )

    def test_finish(self):
        """IK: docs/school_admission/09-finish.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_finish", login="admin"
        )

    def test_cancel(self):
        """IK: docs/school_admission/10-cancel.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_cancel", login="admin"
        )

    def test_restart(self):
        """IK: docs/school_admission/12-restart.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_restart", login="admin"
        )

    def test_reset_number(self):
        """IK: docs/school_admission/13-reset-number.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_reset_number",
            login="admin",
        )

    def test_restart_approval(self):
        """IK: docs/school_admission/14-restart-approval.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_restart_approval",
            login="admin",
        )

    def test_create_due_invoice(self):
        """IK: docs/school_admission/15-create-due-invoice.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_create_due_invoice",
            login="admin",
        )

    def test_create_enrollment(self):
        """Assert the resulting School Enrollment opens.

        IK: docs/school_admission/16-create-enrollment.md

        Boundary (Design Decision of ssi-school#227): only verifies the
        resulting document opens; wizard field values are unit test
        territory.
        """
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_create_enrollment",
            login="admin",
        )

    def test_close_addendum(self):
        """IK: docs/school_admission/17-close-addendum.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_close_addendum",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_admission/18-print.md
        """
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_print", login="admin"
        )

    def test_reload_template_policy(self):
        """IK: docs/school_admission/19-reload-template-policy.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_reload_template_policy",
            login="admin",
        )
