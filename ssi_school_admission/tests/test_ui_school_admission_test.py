# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolAdmissionTest(HttpSavepointCase):
    """UI/UX tour tests for the ``school_admission_test`` work
    instructions.

    Every ``test_*`` method runs the tour pairing with the IK file named
    in its docstring (``docs/school_admission_test/NN-*.md``).
    """

    @classmethod
    def setUpClass(cls):
        """Build the academic/school structure and one fixture per tour."""
        super().setUpClass()

        # SavepointCase.setUpClass runs cls.env as SUPERUSER_ID (odoo/
        # tests/common.py), so any record created via cls.env.create()
        # without an explicit user_id defaults "Responsible" (user_id,
        # mixin.transaction._default_user_id -> self.env.user.id) to the
        # superuser, NOT "admin". school_admission_test_internal_user_rule
        # ([('user_id','=',user.id)], base.group_user) then hides every
        # such fixture from the "admin" tour session -- 0 rows in every
        # list, no crash. Every fixture below sets user_id explicitly.
        cls.admin_user = cls.env.ref("base.user_admin")

        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ADM TEST Academic Year",
                "code": "TOURADMTAY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR ADM TEST Term",
                "code": "TOURADMTT",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.academic_year.id,
            }
        )
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR ADM TEST Grade Type", "code": "TOURADMTGT"}
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR ADM TEST School",
                "code": "TOURADMTSCH",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "TOUR ADM TEST Grade",
                "code": "TOURADMTG",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )

        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR ADM TEST Cancel Reason",
                "code": "TOUR-ADM-TEST-CANCEL",
                "global_use": True,
            }
        )

        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Admission Test Report",
                "model": "school_admission_test",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school_admission.tour_school_admission_test_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Admission Test Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_admission_test"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )

        # Access: the Policies tab (17-reload-template-policy.md) is
        # only visible to base.group_system.
        cls.env.ref("base.group_system").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

        # -- Operating unit (ssi_school_admission_operating_unit) -------
        # When that extension module is installed alongside this one (as
        # it is in the full CI bundle), school_admission_test is gated
        # by an ir.rule restricting visibility to
        # [('operating_unit_id','in',[g.id for g in
        # user.operating_unit_ids])] with no False fallback -- every
        # fixture below sets operating_unit_id explicitly so it stays
        # visible to the "admin" tour session. Guarded by a registry
        # check so this module's own tests keep working standalone.
        cls.operating_unit = False
        if "operating.unit" in cls.env:
            ou_partner = cls.env["res.partner"].create(
                {"name": "TOUR ADM TEST OU Partner"}
            )
            cls.operating_unit = cls.env["operating.unit"].create(
                {
                    "name": "TOUR ADM TEST Operating Unit",
                    "code": "TOURADMTOU",
                    "partner_id": ou_partner.id,
                }
            )
            cls.env.ref("base.user_admin").sudo().write(
                {
                    "assigned_operating_unit_ids": [(4, cls.operating_unit.id)],
                    "default_operating_unit_id": cls.operating_unit.id,
                }
            )

        def _create_test(student_name):
            """Create a Draft ``school_admission_test`` fixture."""
            student = cls.env["res.partner"].create({"name": student_name})
            vals = {
                "academic_year_id": cls.academic_year.id,
                "academic_term_id": cls.academic_term.id,
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "student_id": student.id,
                "user_id": cls.admin_user.id,
            }
            if cls.operating_unit:
                vals["operating_unit_id"] = cls.operating_unit.id
            return cls.env["school_admission_test"].create(vals)

        def _bypass(record):
            """Advance a fixture past a policy gate as Pre-Condition setup."""
            return record.with_context(bypass_policy_check=True)

        # 01-create.md -- eligible Student to pick from the dropdown.
        cls.student_create = cls.env["res.partner"].create(
            {"name": "TOUR ADM TEST Create Student"}
        )

        # NOTE: every fixture below is named with an ``admission_test_``
        # prefix -- NEVER bare ``test_<action>`` -- because a class
        # attribute named exactly like one of this class's own
        # ``test_*`` methods (e.g. ``cls.test_edit`` next to
        # ``def test_edit(self)``) overwrites/shadows that method on the
        # class. unittest then tries to call the shadowed attribute (a
        # recordset) as the test, raising "TypeError: '<model>' object
        # is not callable" for every affected method. Verified in CI on
        # PR #250 (commit 13454c5): every method whose fixture shared
        # its exact name failed this way; ``test_create`` (fixture
        # ``cls.student_create``) and ``test_create_school_admission``
        # (fixture ``cls.admission_test_create_admission``, a
        # deliberately different name) were unaffected.

        # 02-edit.md
        cls.admission_test_edit = _create_test("TOUR ADM TEST Edit Student")

        # 03-delete.md
        cls.admission_test_delete = _create_test("TOUR ADM TEST Delete Student")

        # 04-confirm.md
        cls.admission_test_confirm = _create_test("TOUR ADM TEST Confirm Student")

        # 05-approve.md
        cls.admission_test_approve = _create_test("TOUR ADM TEST Approve Student")
        _bypass(cls.admission_test_approve).action_confirm()

        # 06-reject.md
        cls.admission_test_reject = _create_test("TOUR ADM TEST Reject Student")
        _bypass(cls.admission_test_reject).action_confirm()

        # 09-finish.md -- On Progress record to finish.
        cls.admission_test_finish = _create_test("TOUR ADM TEST Finish Student")
        _bypass(cls.admission_test_finish).action_confirm()
        _bypass(cls.admission_test_finish).action_approve_approval()

        # 10-cancel.md
        cls.admission_test_cancel = _create_test("TOUR ADM TEST Cancel Student")

        # 12-restart.md -- Rejected record to restart.
        cls.admission_test_restart = _create_test("TOUR ADM TEST Restart Student")
        _bypass(cls.admission_test_restart).action_confirm()
        _bypass(cls.admission_test_restart).action_reject_approval()
        if cls.admission_test_restart.state != "reject":
            cls.admission_test_restart.sudo().write({"state": "reject"})

        # 13-reset-number.md
        cls.admission_test_reset_number = _create_test(
            "TOUR ADM TEST Reset Number Student"
        )
        cls.admission_test_reset_number.write({"name": "TOUR-ADM-TEST-MANUAL-001"})

        # 14-restart-approval.md
        cls.admission_test_restart_approval = _create_test(
            "TOUR ADM TEST Restart Approval Student"
        )
        _bypass(cls.admission_test_restart_approval).action_confirm()

        # 15-create-school-admission.md -- Done and Passed.
        cls.admission_test_create_admission = _create_test(
            "TOUR ADM TEST Create Admission Student"
        )
        _bypass(cls.admission_test_create_admission).action_confirm()
        _bypass(cls.admission_test_create_admission).action_approve_approval()
        cls.admission_test_create_admission.write({"passed": True})
        _bypass(cls.admission_test_create_admission).action_done()

        # 16-print.md
        cls.admission_test_print = _create_test("TOUR ADM TEST Print Student")

        # 17-reload-template-policy.md
        cls.admission_test_reload_policy = _create_test(
            "TOUR ADM TEST Reload Policy Student"
        )
        cls.admission_test_reload_policy.write({"policy_template_id": False})

    def test_create(self):
        """IK: docs/school_admission_test/01-create.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_test_create", login="admin"
        )

    def test_edit(self):
        """IK: docs/school_admission_test/02-edit.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_test_edit", login="admin"
        )

    def test_delete(self):
        """IK: docs/school_admission_test/03-delete.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_test_delete", login="admin"
        )

    def test_confirm(self):
        """IK: docs/school_admission_test/04-confirm.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_test_confirm", login="admin"
        )

    def test_approve(self):
        """IK: docs/school_admission_test/05-approve.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_test_approve", login="admin"
        )

    def test_reject(self):
        """IK: docs/school_admission_test/06-reject.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_test_reject", login="admin"
        )

    def test_finish(self):
        """IK: docs/school_admission_test/09-finish.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_test_finish", login="admin"
        )

    def test_cancel(self):
        """IK: docs/school_admission_test/10-cancel.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_test_cancel", login="admin"
        )

    def test_restart(self):
        """IK: docs/school_admission_test/12-restart.md"""
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_test_restart", login="admin"
        )

    def test_reset_number(self):
        """IK: docs/school_admission_test/13-reset-number.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_test_reset_number",
            login="admin",
        )

    def test_restart_approval(self):
        """IK: docs/school_admission_test/14-restart-approval.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_test_restart_approval",
            login="admin",
        )

    def test_create_school_admission(self):
        """Assert the resulting School Admission opens.

        IK: docs/school_admission_test/15-create-school-admission.md

        Boundary (Design Decision of ssi-school#227): only verifies the
        resulting document opens; wizard field values are unit test
        territory.
        """
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_test_create_school_admission",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_admission_test/16-print.md
        """
        self.start_tour(
            "/web", "ssi_school_admission_school_admission_test_print", login="admin"
        )

    def test_reload_template_policy(self):
        """IK: docs/school_admission_test/17-reload-template-policy.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_test_reload_template_policy",
            login="admin",
        )
