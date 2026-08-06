# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolEnrollment(HttpSavepointCase):
    """Tour tests for the ``school_enrollment`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create every record the school_enrollment tours click through.

        Builds, in order: accounting basics (journal/account/customer
        invoice type/product/pricelist), the academic structure (grade
        type, one academic year with two open terms -- the first not
        last, the second last -- school, two grades, two grade classes),
        a payment template scoped to the first term, a test-only
        ``policy.template_detail`` granting ``restart_approval_ok`` (the
        shipped ``policy_template_school_enrollment`` has no detail for
        that field -- see the blocker note in the final report), a
        cancel reason, a print document type, and finally one
        ``school_enrollment`` fixture per tour, each advanced to the
        state its Pre-Condition requires via
        ``bypass_policy_check=True`` (mirroring
        ``employee_external_assignment``'s test setup) since the admin
        identity ``cls.env`` runs as during setup is not guaranteed to
        be registered as an approver the same way the browser's
        ``login="admin"`` session is.
        """
        super().setUpClass()

        # -- Accounting basics -------------------------------------------------
        cls.ci_journal = cls.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        receivable_type = cls.env.ref("account.data_account_type_receivable")
        cls.ci_account = cls.env["account.account"].create(
            {
                "name": "TOUR ENR Receivable",
                "code": "TOURENRRCV",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        cls.ci_type = cls.env["customer_invoice_type"].create(
            {
                "name": "TOUR ENR CI Type",
                "code": "TOURENRCIT",
                "journal_id": cls.ci_journal.id,
                "receivable_account_id": cls.ci_account.id,
            }
        )
        income_type = cls.env.ref("account.data_account_type_revenue")
        cls.income_account = cls.env["account.account"].create(
            {
                "name": "TOUR ENR Income",
                "code": "TOURENRINC",
                "user_type_id": income_type.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "TOUR ENR Fee",
                "type": "service",
                "list_price": 1_000_000.0,
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "TOUR ENR Pricelist",
                "currency_id": cls.env.company.currency_id.id,
            }
        )

        # -- Academic structure --------------------------------------------
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR ENR Grade Type",
                "code": "TOURENRGT",
            }
        )
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ENR Academic Year",
                "code": "TOURENRAY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        # Created first / earliest date_start -> first_term=True,
        # last_term=False (used by every fixture EXCEPT 15/16/17/18,
        # which require last_term=True -- see academic_term_2 below).
        cls.academic_term_1 = cls.env["school_academic_term"].create(
            {
                "name": "TOUR ENR Term 1",
                "code": "TOURENRT1",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.academic_year.id,
                "enrollment_state": "open",
            }
        )
        # Created second / latest date_start -> last_term=True.
        cls.academic_term_2 = cls.env["school_academic_term"].create(
            {
                "name": "TOUR ENR Term 2",
                "code": "TOURENRT2",
                "date_start": "2025-01-01",
                "date_end": "2025-06-30",
                "year_id": cls.academic_year.id,
                "enrollment_state": "open",
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR ENR School",
                "code": "TOURENRSCH",
                "grade_type_id": cls.grade_type.id,
            }
        )
        # Lowest sequence -> auto-picked as a fresh student's next_grade_id.
        cls.grade_1 = cls.env["school_grade"].create(
            {
                "name": "TOUR ENR Grade 1",
                "code": "TOURENRG1",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        # grade_1.next_grade_id after grade_2 is created (used by 15-pass
        # Post-Condition: Promote To Grade = Grade's configured next grade).
        cls.grade_2 = cls.env["school_grade"].create(
            {
                "name": "TOUR ENR Grade 2",
                "code": "TOURENRG2",
                "sequence": 20,
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_class_a = cls.env["school_grade_class"].create(
            {
                "name": "TOUR ENR Class A",
                "code": "TOURENRCA",
                "school_id": cls.school.id,
                "grade_id": cls.grade_1.id,
            }
        )
        # Second homeroom class, used by 02-edit to change grade_class_id
        # to a different valid value ("Change the required fields").
        cls.grade_class_b = cls.env["school_grade_class"].create(
            {
                "name": "TOUR ENR Class B",
                "code": "TOURENRCB",
                "school_id": cls.school.id,
                "grade_id": cls.grade_1.id,
            }
        )

        # -- Payment template (scoped to term 1 / school / grade 1) --------
        cls.payment_template = cls.env["school_enrollment_payment_template"].create(
            {
                "name": "TOUR ENR Payment Template",
                "code": "TOURENRPMT",
                "customer_invoice_type_id": cls.ci_type.id,
                "school_id": cls.school.id,
                "grade_id": cls.grade_1.id,
                "academic_term_id": cls.academic_term_1.id,
                "term_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "TOUR ENR PMT Term",
                            "sequence": 10,
                            "detail_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "product_id": cls.product.id,
                                        "name": "TOUR ENR PMT Detail",
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

        # -- Policy: grant restart_approval_ok (14-restart-approval.md) ----
        # The module's shipped policy_template_school_enrollment has NO
        # policy.template_detail for restart_approval_ok, so that field is
        # always False out of the box (see the blocker note in the final
        # report). Add a test-only detail on the SAME shipped template so
        # the "Restart Approval Process" button becomes visible while
        # Waiting for Approval, for a user in the User group.
        state_field = cls.env["ir.model.fields"].search(
            [("model_id.model", "=", "school_enrollment"), ("name", "=", "state")],
            limit=1,
        )
        confirm_selection = cls.env["ir.model.fields.selection"].search(
            [("field_id", "=", state_field.id), ("value", "=", "confirm")],
            limit=1,
        )
        restart_approval_field = cls.env["ir.model.fields"].search(
            [
                ("model_id.model", "=", "school_enrollment"),
                ("name", "=", "restart_approval_ok"),
            ],
            limit=1,
        )
        cls.env["policy.template_detail"].create(
            {
                "template_id": cls.env.ref(
                    "ssi_school.policy_template_school_enrollment"
                ).id,
                "field_id": restart_approval_field.id,
                "restrict_state": True,
                "state_ids": [(6, 0, confirm_selection.ids)],
                "restrict_user": True,
                "computation_method": "use_group",
                "group_ids": [
                    (6, 0, [cls.env.ref("ssi_school.school_enrollment_user_group").id])
                ],
                "restrict_additional": False,
            }
        )

        # -- Access: the Policies tab (22-reload-template-policy.md) is
        # only visible to base.group_system.
        cls.env.ref("base.group_system").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

        # -- Cancel reason (10-cancel.md) -----------------------------------
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR ENR Cancel Reason",
                "code": "TOUR-ENR-CANCEL",
                "global_use": True,
            }
        )

        # -- Print document type (21-print.md) ------------------------------
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR ENR Print Report",
                "model": "school_enrollment",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school.tour_school_enrollment_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR ENR Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_enrollment"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )

        def _create_enrollment(student_name, term, grade_class=None):
            """Create a draft ``school_enrollment`` Pre-Condition fixture."""
            # `contact_id` is a required res.partner on school_student
            # (models/school_student.py); without it the create() call
            # below raises a NOT NULL constraint violation.
            contact = cls.env["res.partner"].create({"name": student_name})
            student = cls.env["school_student"].create(
                {
                    "name": student_name,
                    "code": "/",
                    "school_id": cls.school.id,
                    "contact_id": contact.id,
                }
            )
            return cls.env["school_enrollment"].create(
                {
                    "academic_year_id": cls.academic_year.id,
                    "academic_term_id": term.id,
                    "school_id": cls.school.id,
                    "grade_id": cls.grade_1.id,
                    "grade_class_id": (grade_class or cls.grade_class_a).id,
                    "student_id": student.id,
                    "currency_id": cls.env.company.currency_id.id,
                    "customer_invoice_type_id": cls.ci_type.id,
                    "receivable_journal_id": cls.ci_journal.id,
                    "receivable_account_id": cls.ci_account.id,
                }
            )

        def _bypass(record):
            """Advance a fixture past a policy gate as Pre-Condition setup."""
            return record.with_context(bypass_policy_check=True)

        # 01-create.md -- no pre-existing record; the create tour builds a
        # new one on term 1 (first term), but needs an eligible student
        # (Draft, next_grade_id auto-computed to grade_1) to pick from the
        # Student dropdown.
        cls.contact_create_student = cls.env["res.partner"].create(
            {"name": "TOUR ENR Create Student"}
        )
        cls.student_create = cls.env["school_student"].create(
            {
                "name": "TOUR ENR Create Student",
                "code": "/",
                "school_id": cls.school.id,
                "contact_id": cls.contact_create_student.id,
            }
        )

        # 02-edit.md -- Draft record to edit.
        cls.enrollment_edit = _create_enrollment(
            "TOUR ENR Edit Student", cls.academic_term_1, cls.grade_class_a
        )

        # 03-delete.md -- Draft record, document number still "/".
        cls.enrollment_delete = _create_enrollment(
            "TOUR ENR Delete Student", cls.academic_term_1
        )

        # 04-confirm.md -- Draft record to confirm.
        cls.enrollment_confirm = _create_enrollment(
            "TOUR ENR Confirm Student", cls.academic_term_1
        )

        # 05-approve.md -- Waiting for Approval record to approve.
        cls.enrollment_approve = _create_enrollment(
            "TOUR ENR Approve Student", cls.academic_term_1
        )
        _bypass(cls.enrollment_approve).action_confirm()

        # 06-reject.md -- Waiting for Approval record to reject.
        cls.enrollment_reject = _create_enrollment(
            "TOUR ENR Reject Student", cls.academic_term_1
        )
        _bypass(cls.enrollment_reject).action_confirm()

        # 09-finish.md -- On Progress record on term 1 (NOT last term).
        cls.enrollment_finish = _create_enrollment(
            "TOUR ENR Finish Student", cls.academic_term_1
        )
        _bypass(cls.enrollment_finish).action_confirm()
        _bypass(cls.enrollment_finish).action_approve_approval()

        # 10-cancel.md -- On Progress record to cancel (no invoiced terms).
        cls.enrollment_cancel = _create_enrollment(
            "TOUR ENR Cancel Student", cls.academic_term_1
        )
        _bypass(cls.enrollment_cancel).action_confirm()
        _bypass(cls.enrollment_cancel).action_approve_approval()

        # 12-restart.md -- Rejected record to restart.
        cls.enrollment_restart = _create_enrollment(
            "TOUR ENR Restart Student", cls.academic_term_1
        )
        _bypass(cls.enrollment_restart).action_confirm()
        # action_reject_approval() (mixin.multiple_approval) only
        # writes state="reject" when the acting user is found in
        # active_approval_ids.approver_user_ids -- a real membership
        # list computed from the approval.approval record created by
        # action_confirm(), NOT simply from holding
        # school_enrollment_validator_group. bypass_policy_check only
        # skips the outer _check_reject_policy() gate, not this inner
        # filter, so it silently no-ops when admin isn't in that list.
        # Force the Pre-Condition state directly instead -- this tour
        # exercises action_restart, not the reject transition itself
        # (that is covered by 06-reject.md's own tour).
        _bypass(cls.enrollment_restart).action_reject_approval()
        if cls.enrollment_restart.state != "reject":
            cls.enrollment_restart.sudo().write({"state": "reject"})

        # 13-reset-number.md -- Draft record with a manually-set document
        # number (the "name" field is editable in Draft status).
        cls.enrollment_reset_number = _create_enrollment(
            "TOUR ENR Reset Number Student", cls.academic_term_1
        )
        cls.enrollment_reset_number.write({"name": "TOUR-ENR-MANUAL-001"})

        # 14-restart-approval.md -- Waiting for Approval record whose
        # approval process will be rebuilt.
        cls.enrollment_restart_approval = _create_enrollment(
            "TOUR ENR Restart Approval Student", cls.academic_term_1
        )
        _bypass(cls.enrollment_restart_approval).action_confirm()

        # 15-pass.md / 16-fail.md / 17-drop-out.md / 18-graduate.md -- On
        # Progress records on term 2 (the LAST term of the academic year).
        cls.enrollment_pass = _create_enrollment(
            "TOUR ENR Pass Student", cls.academic_term_2
        )
        _bypass(cls.enrollment_pass).action_confirm()
        _bypass(cls.enrollment_pass).action_approve_approval()

        cls.enrollment_fail = _create_enrollment(
            "TOUR ENR Fail Student", cls.academic_term_2
        )
        _bypass(cls.enrollment_fail).action_confirm()
        _bypass(cls.enrollment_fail).action_approve_approval()

        cls.enrollment_drop_out = _create_enrollment(
            "TOUR ENR Drop Out Student", cls.academic_term_2
        )
        _bypass(cls.enrollment_drop_out).action_confirm()
        _bypass(cls.enrollment_drop_out).action_approve_approval()

        cls.enrollment_graduate = _create_enrollment(
            "TOUR ENR Graduate Student", cls.academic_term_2
        )
        _bypass(cls.enrollment_graduate).action_confirm()
        _bypass(cls.enrollment_graduate).action_approve_approval()

        # 19-create-due-invoice.md -- On Progress record with one
        # Uninvoiced payment term whose Estimated Invoice Date is today.
        cls.enrollment_invoice = _create_enrollment(
            "TOUR ENR Invoice Student", cls.academic_term_1
        )
        _bypass(cls.enrollment_invoice).action_confirm()
        _bypass(cls.enrollment_invoice).action_approve_approval()
        # IK Pre-Condition says "on or before the date range used in
        # the wizard", not "exactly today" -- use yesterday rather
        # than today so the comparison in
        # school_enrollment._get_due_payment_term() (which defaults
        # date_end to fields.Date.context_today(), TIMEZONE-AWARE)
        # cannot fail a same-day boundary check against
        # fields.Date.today() (server-local, NOT timezone-adjusted).
        cls.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": cls.enrollment_invoice.id,
                "name": "TOUR ENR DUE TERM",
                "sequence": 10,
                "date_invoice": fields.Date.today() - timedelta(days=1),
            }
        )

        # 20-close-addendum.md -- On Progress record with one currently
        # UNLOCKED payment term. Post-open locking only affects terms that
        # existed BEFORE the enrollment opened, so this term is added
        # afterwards to simulate an addendum line.
        cls.enrollment_addendum = _create_enrollment(
            "TOUR ENR Addendum Student", cls.academic_term_1
        )
        _bypass(cls.enrollment_addendum).action_confirm()
        _bypass(cls.enrollment_addendum).action_approve_approval()
        cls.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": cls.enrollment_addendum.id,
                "name": "TOUR ENR ADDENDUM TERM",
                "sequence": 10,
            }
        )

        # 21-print.md -- any record; Print does not depend on status.
        cls.enrollment_print = _create_enrollment(
            "TOUR ENR Print Student", cls.academic_term_1
        )

        # 22-reload-template-policy.md -- record with policy_template_id
        # cleared beforehand, so reloading produces an observable change
        # (the field goes from empty to showing "Standard").
        cls.enrollment_reload_policy = _create_enrollment(
            "TOUR ENR Reload Policy Student", cls.academic_term_1
        )
        cls.enrollment_reload_policy.write({"policy_template_id": False})

        # 24-copy-payment-term.md -- a Draft source (carrying one payment
        # term) and a Draft target (with none yet), sharing the same
        # academic term / school / grade. The wizard's Source Enrollment
        # field searches school_enrollment's own display name (the
        # document number), which is "*<id>" while still "/" -- not the
        # student name -- so a distinctive manual number is set here to
        # make the source text-searchable in the tour (same technique as
        # 13-reset-number.md).
        cls.enrollment_copy_source = _create_enrollment(
            "TOUR ENR Copy Source Student", cls.academic_term_1
        )
        cls.enrollment_copy_source.write({"name": "TOUR-ENR-COPY-SOURCE-001"})
        cls.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": cls.enrollment_copy_source.id,
                "name": "TOUR ENR COPY TERM",
                "sequence": 10,
            }
        )
        cls.enrollment_copy_target = _create_enrollment(
            "TOUR ENR Copy Target Student", cls.academic_term_1
        )

    def test_create(self):
        """IK: docs/school_enrollment/01-create.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_create", login="admin")

    def test_edit(self):
        """IK: docs/school_enrollment/02-edit.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_edit", login="admin")

    def test_delete(self):
        """IK: docs/school_enrollment/03-delete.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_delete", login="admin")

    def test_confirm(self):
        """IK: docs/school_enrollment/04-confirm.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_confirm", login="admin")

    def test_approve(self):
        """IK: docs/school_enrollment/05-approve.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_approve", login="admin")

    def test_reject(self):
        """IK: docs/school_enrollment/06-reject.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_reject", login="admin")

    def test_finish(self):
        """IK: docs/school_enrollment/09-finish.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_finish", login="admin")

    def test_cancel(self):
        """IK: docs/school_enrollment/10-cancel.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_cancel", login="admin")

    def test_restart(self):
        """IK: docs/school_enrollment/12-restart.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_restart", login="admin")

    def test_reset_number(self):
        """IK: docs/school_enrollment/13-reset-number.md"""
        self.start_tour(
            "/web", "ssi_school_school_enrollment_reset_number", login="admin"
        )

    def test_restart_approval(self):
        """IK: docs/school_enrollment/14-restart-approval.md"""
        self.start_tour(
            "/web", "ssi_school_school_enrollment_restart_approval", login="admin"
        )

    def test_pass(self):
        """IK: docs/school_enrollment/15-pass.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_pass", login="admin")

    def test_fail(self):
        """IK: docs/school_enrollment/16-fail.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_fail", login="admin")

    def test_drop_out(self):
        """IK: docs/school_enrollment/17-drop-out.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_drop_out", login="admin")

    def test_graduate(self):
        """IK: docs/school_enrollment/18-graduate.md"""
        self.start_tour("/web", "ssi_school_school_enrollment_graduate", login="admin")

    def test_create_due_invoice(self):
        """IK: docs/school_enrollment/19-create-due-invoice.md"""
        self.start_tour(
            "/web", "ssi_school_school_enrollment_create_due_invoice", login="admin"
        )

    def test_close_addendum(self):
        """IK: docs/school_enrollment/20-close-addendum.md"""
        self.start_tour(
            "/web", "ssi_school_school_enrollment_close_addendum", login="admin"
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_enrollment/21-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour("/web", "ssi_school_school_enrollment_print", login="admin")

    def test_reload_template_policy(self):
        """IK: docs/school_enrollment/22-reload-template-policy.md"""
        self.start_tour(
            "/web",
            "ssi_school_school_enrollment_reload_template_policy",
            login="admin",
        )

    def test_copy_payment_term(self):
        """IK: docs/school_enrollment/24-copy-payment-term.md"""
        self.start_tour(
            "/web", "ssi_school_school_enrollment_copy_payment_term", login="admin"
        )
