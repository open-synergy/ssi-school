# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolAdmissionForm(HttpSavepointCase):
    """UI/UX tour tests for the ``school_admission_form`` work
    instructions.

    Every ``test_*`` method runs the tour pairing with the IK file named
    in its docstring (``docs/school_admission_form/NN-*.md``).
    Pre-Condition data is prepared here in Python, never through UI
    steps, and fixtures are advanced past a policy gate with
    ``bypass_policy_check=True`` since the admin identity ``cls.env``
    runs as during setup is not guaranteed to be registered as an
    approver the same way the browser's ``login="admin"`` session is
    (mirrors ``test_ui_school_enrollment.py``).
    """

    @classmethod
    def setUpClass(cls):
        """Build the academic/school structure and one fixture per tour."""
        super().setUpClass()

        # SavepointCase.setUpClass runs cls.env as SUPERUSER_ID (odoo/
        # tests/common.py), so any record created via cls.env.create()
        # without an explicit user_id defaults "Responsible" (user_id,
        # mixin.transaction._default_user_id -> self.env.user.id) to the
        # superuser, NOT "admin". school_admission_form_internal_user_rule
        # ([('user_id','=',user.id)], base.group_user) then hides every
        # such fixture from the "admin" tour session -- 0 rows in every
        # list, no crash. Every fixture below sets user_id explicitly.
        cls.admin_user = cls.env.ref("base.user_admin")

        # -- Academic / school structure -------------------------------
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ADM FORM Academic Year",
                "code": "TOURADMFAY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR ADM FORM Term",
                "code": "TOURADMFT",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.academic_year.id,
            }
        )
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR ADM FORM Grade Type", "code": "TOURADMFGT"}
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR ADM FORM School",
                "code": "TOURADMFSCH",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "TOUR ADM FORM Grade",
                "code": "TOURADMFG",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        # 02-edit.md -- a second grade so the edit tour changes grade_id
        # to a value DIFFERENT from what form_edit was created with.
        cls.grade_b = cls.env["school_grade"].create(
            {
                "name": "TOUR ADM FORM Grade B",
                "code": "TOURADMFGB",
                "sequence": 20,
                "type_id": cls.grade_type.id,
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "TOUR ADM FORM Pricelist",
                "currency_id": cls.env.company.currency_id.id,
            }
        )
        cls.parent = cls.env["res.partner"].create(
            {"name": "TOUR ADM FORM Parent", "is_company": True}
        )

        # -- Fee template (01-create.md / 02-edit.md) -------------------
        income_type = cls.env.ref("account.data_account_type_revenue")
        cls.income_account = cls.env["account.account"].create(
            {
                "name": "TOUR ADM FORM Income",
                "code": "TOURADMFINC",
                "user_type_id": income_type.id,
            }
        )
        # journal_id/account_id are required=True on school_admission_form
        # (inherited from mixin.account_move -- ssi_accounting_entry_mixin).
        # The UI fills them via onchange_journal_id/onchange_account_id
        # when Fee Template is selected on the form, but those onchanges
        # never fire on a plain Python .create() call, so every fixture
        # built by _create_form() below sets them explicitly.
        cls.journal = cls.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        cls.fee_product = cls.env["product.product"].create(
            {"name": "TOUR ADM FORM Fee Product"}
        )
        cls.fee_template = cls.env["school_admission_fee_template"].create(
            {
                "name": "TOUR ADM FORM Fee Template",
                "code": "TOURADMFFT",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "journal_id": cls.journal.id,
                "account_id": cls.income_account.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.fee_product.id,
                            "name": "TOUR ADM FORM Fee Line",
                            "account_id": cls.income_account.id,
                            "uom_quantity": 1,
                            "uom_id": cls.env.ref("uom.product_uom_unit").id,
                            "price_unit": 1_000_000.0,
                        },
                    )
                ],
            }
        )

        # -- Operating unit (ssi_school_admission_operating_unit) -------
        # When that extension module is installed alongside this one (as
        # it is in the full CI bundle), school_admission_form is gated
        # by an ir.rule restricting visibility to
        # [('operating_unit_id','in',[g.id for g in
        # user.operating_unit_ids])] with no False fallback. Every
        # fixture below sets operating_unit_id explicitly so it stays
        # visible to the "admin" tour session. Guarded by a registry
        # check so this module's own tests keep working standalone (the
        # "operating.unit" model only exists once that extension is
        # installed).
        cls.operating_unit = False
        if "operating.unit" in cls.env:
            ou_partner = cls.env["res.partner"].create(
                {"name": "TOUR ADM FORM OU Partner"}
            )
            cls.operating_unit = cls.env["operating.unit"].create(
                {
                    "name": "TOUR ADM FORM Operating Unit",
                    "code": "TOURADMFOU",
                    "partner_id": ou_partner.id,
                }
            )
            cls.env.ref("base.user_admin").sudo().write(
                {
                    "assigned_operating_unit_ids": [(4, cls.operating_unit.id)],
                    "default_operating_unit_id": cls.operating_unit.id,
                }
            )

        # -- Cancel reason (10-cancel.md) --------------------------------
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR ADM FORM Cancel Reason",
                "code": "TOUR-ADM-FORM-CANCEL",
                "global_use": True,
            }
        )

        # -- Print document type (17-print.md) ---------------------------
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Admission Form Report",
                "model": "school_admission_form",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school_admission.tour_school_admission_form_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Admission Form Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_admission_form"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )

        # -- Access: the Policies tab (18-reload-template-policy.md) is
        # only visible to base.group_system.
        cls.env.ref("base.group_system").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

        def _create_form(student_name, free=False):
            """Create a Draft ``school_admission_form`` fixture.

            ``journal_id``/``account_id``/``currency_id`` are
            required=True on base mixins (``mixin.account_move``,
            ``mixin.transaction_total``/``_tax``/``_untaxed``) and are
            normally filled by onchange (``onchange_journal_id`` /
            ``onchange_account_id``; the ``currency_id`` field is itself
            ``related="pricelist_id.currency_id", store=True`` but a
            required related-stored field can still be inserted before
            its compute runs on a plain ``.create()`` call) -- so all
            three are always set explicitly here, free or not.

            :param free: when True, no fee template/lines are set, so
                the total is zero and approval auto-cascades all the way
                to Done via ``_20_auto_done_if_free``.
            """
            student = cls.env["res.partner"].create({"name": student_name})
            vals = {
                "academic_year_id": cls.academic_year.id,
                "academic_term_id": cls.academic_term.id,
                "student_id": student.id,
                "parent_id": cls.parent.id,
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "pricelist_id": cls.pricelist.id,
                "currency_id": cls.pricelist.currency_id.id,
                "journal_id": cls.journal.id,
                "account_id": cls.income_account.id,
                "user_id": cls.admin_user.id,
            }
            if cls.operating_unit:
                vals["operating_unit_id"] = cls.operating_unit.id
            if not free:
                vals["fee_template_id"] = cls.fee_template.id
            form = cls.env["school_admission_form"].create(vals)
            if not free:
                form._compute_fee_from_template()
            return form

        def _bypass(record):
            """Advance a fixture past a policy gate as Pre-Condition setup."""
            return record.with_context(bypass_policy_check=True)

        # 01-create.md -- no pre-existing record; an eligible Student
        # (res.partner) to pick from the dropdown.
        cls.student_create = cls.env["res.partner"].create(
            {"name": "TOUR ADM FORM Create Student"}
        )

        # 02-edit.md
        cls.form_edit = _create_form("TOUR ADM FORM Edit Student")

        # 03-delete.md
        cls.form_delete = _create_form("TOUR ADM FORM Delete Student")

        # 04-confirm.md
        cls.form_confirm = _create_form("TOUR ADM FORM Confirm Student")

        # 05-approve.md -- FREE form so approval lands directly on Done.
        cls.form_approve = _create_form("TOUR ADM FORM Approve Student", free=True)
        _bypass(cls.form_approve).action_confirm()

        # 06-reject.md
        cls.form_reject = _create_form("TOUR ADM FORM Reject Student")
        _bypass(cls.form_reject).action_confirm()

        # 10-cancel.md
        cls.form_cancel = _create_form("TOUR ADM FORM Cancel Student")

        # 12-restart.md -- Rejected record to restart.
        cls.form_restart = _create_form("TOUR ADM FORM Restart Student")
        _bypass(cls.form_restart).action_confirm()
        _bypass(cls.form_restart).action_reject_approval()
        if cls.form_restart.state != "reject":
            cls.form_restart.sudo().write({"state": "reject"})

        # 13-reset-number.md -- Draft record with a manually-set number.
        cls.form_reset_number = _create_form("TOUR ADM FORM Reset Number Student")
        cls.form_reset_number.write({"name": "TOUR-ADM-FORM-MANUAL-001"})

        # 14-restart-approval.md
        cls.form_restart_approval = _create_form(
            "TOUR ADM FORM Restart Approval Student"
        )
        _bypass(cls.form_restart_approval).action_confirm()

        # 15-create-admission.md / 16-create-admission-test.md -- Done,
        # FREE forms (no reconciliation needed to reach Done).
        cls.form_create_admission = _create_form(
            "TOUR ADM FORM Create Admission Student", free=True
        )
        _bypass(cls.form_create_admission).action_confirm()
        _bypass(cls.form_create_admission).action_approve_approval()

        cls.form_create_test = _create_form(
            "TOUR ADM FORM Create Test Student", free=True
        )
        _bypass(cls.form_create_test).action_confirm()
        _bypass(cls.form_create_test).action_approve_approval()

        # 17-print.md -- any record; Print does not depend on status.
        cls.form_print = _create_form("TOUR ADM FORM Print Student")

        # 18-reload-template-policy.md -- policy_template_id cleared
        # beforehand, so reloading produces an observable change.
        cls.form_reload_policy = _create_form("TOUR ADM FORM Reload Policy Student")
        cls.form_reload_policy.write({"policy_template_id": False})

    def test_create(self):
        """IK: docs/school_admission_form/01-create.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_form_create", login="admin"
        )

    def test_edit(self):
        """IK: docs/school_admission_form/02-edit.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_form_edit", login="admin"
        )

    def test_delete(self):
        """IK: docs/school_admission_form/03-delete.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_form_delete", login="admin"
        )

    def test_confirm(self):
        """IK: docs/school_admission_form/04-confirm.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_form_confirm", login="admin"
        )

    def test_approve(self):
        """IK: docs/school_admission_form/05-approve.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_form_approve", login="admin"
        )

    def test_reject(self):
        """IK: docs/school_admission_form/06-reject.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_form_reject", login="admin"
        )

    def test_cancel(self):
        """IK: docs/school_admission_form/10-cancel.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_form_cancel", login="admin"
        )

    def test_restart(self):
        """IK: docs/school_admission_form/12-restart.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_form_restart", login="admin"
        )

    def test_reset_number(self):
        """IK: docs/school_admission_form/13-reset-number.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_form_reset_number",
            login="admin",
        )

    def test_restart_approval(self):
        """IK: docs/school_admission_form/14-restart-approval.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_form_restart_approval",
            login="admin",
        )

    def test_create_admission(self):
        """Assert the resulting School Admission opens.

        IK: docs/school_admission_form/15-create-admission.md

        Boundary (Design Decision of ssi-school#227): only verifies the
        resulting document opens; wizard field values are unit test
        territory.
        """
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_form_create_admission",
            login="admin",
        )

    def test_create_admission_test(self):
        """Assert the resulting Admission Test opens.

        IK: docs/school_admission_form/16-create-admission-test.md

        Boundary (Design Decision of ssi-school#227): only verifies the
        resulting document opens; document count/content is unit test
        territory.
        """
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_form_create_admission_test",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_admission_form/17-print.md
        """
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_form_print", login="admin"
        )

    def test_reload_template_policy(self):
        """IK: docs/school_admission_form/18-reload-template-policy.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_form_reload_template_policy",
            login="admin",
        )
