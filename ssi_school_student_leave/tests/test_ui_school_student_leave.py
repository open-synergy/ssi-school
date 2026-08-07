# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolStudentLeave(HttpSavepointCase):
    """Tour tests for the ``school_student_leave`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create every Pre-Condition fixture required by the 13 tours.

        Each tour gets its own isolated grade type / school / grade /
        grade class / academic year & term(s) / student, brought to
        the Enrolled state via ``_create_open_enrollment``, so
        state-changing tours (confirm, approve, reject, cancel,
        restart, return, ...) never interfere with each other's data.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Config Pre-Condition shared by 10-cancel.md: a cancel reason
        # usable on any model.
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR SL Cancel Reason",
                "code": "TOUR-SL-CANCEL",
                "global_use": True,
            }
        )

        # Config Pre-Condition for 16-print.md.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Student Leave Report",
                "model": "school_student_leave",
                "report_type": "qweb-pdf",
                "report_name": (
                    "ssi_school_student_leave.tour_school_student_leave_report"
                ),
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR SL Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_student_leave"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )

        # Config Pre-Condition for 14-restart-approval.md -- same
        # reasoning as ssi_school's test_ui_school_student_mutation.py:
        # policy_template/school_student_leave.xml does not ship a
        # policy.template_detail granting restart_approval_ok, so it
        # is supplied here directly.
        policy_template = cls.env.ref(
            "ssi_school_student_leave.policy_template_school_student_leave"
        )
        state_field = cls.env["ir.model.fields"].search(
            [
                ("model_id.model", "=", "school_student_leave"),
                ("name", "=", "state"),
            ],
            limit=1,
        )
        state_confirm = cls.env["ir.model.fields.selection"].search(
            [
                ("field_id", "=", state_field.id),
                ("value", "=", "confirm"),
            ],
            limit=1,
        )
        restart_approval_field = cls.env["ir.model.fields"].search(
            [
                ("model_id.model", "=", "school_student_leave"),
                ("name", "=", "restart_approval_ok"),
            ],
            limit=1,
        )
        user_group = cls.env.ref(
            "ssi_school_student_leave.school_student_leave_user_group"
        )
        cls.env["policy.template_detail"].create(
            {
                "template_id": policy_template.id,
                "field_id": restart_approval_field.id,
                "restrict_state": True,
                "state_ids": [(6, 0, state_confirm.ids)],
                "restrict_user": True,
                "computation_method": "use_group",
                "group_ids": [(6, 0, [user_group.id])],
                "restrict_additional": False,
            }
        )

        # 01-create.md -- no leave record is pre-created; the create
        # tour creates a new one. It needs an Enrolled student and a
        # second academic term to pick from the list.
        data_cr = cls._create_open_enrollment("CR", "Create")
        cls.term_create_target = cls.env["school_academic_term"].create(
            {
                "name": "TOUR SL Create Term",
                "code": "TMSLCR2",
                "date_start": "2025-01-01",
                "date_end": "2025-06-30",
                "year_id": data_cr["year"].id,
                "enrollment_state": "open",
            }
        )

        # 02-edit.md -- Draft record to edit, plus a second Academic
        # Term the tour switches to.
        data_ed = cls._create_open_enrollment("ED", "Edit")
        cls.term_edit_target = cls.env["school_academic_term"].create(
            {
                "name": "TOUR SL Edit Target Term",
                "code": "TMSLED2",
                "date_start": "2025-01-01",
                "date_end": "2025-06-30",
                "year_id": data_ed["year"].id,
                "enrollment_state": "open",
            }
        )
        cls.leave_edit = cls._create_leave(data_ed)

        # 03-delete.md -- Draft record to delete.
        data_dl = cls._create_open_enrollment("DL", "Delete")
        cls.leave_delete = cls._create_leave(data_dl)

        # 04-confirm.md -- Draft record to confirm.
        data_co = cls._create_open_enrollment("CO", "Confirm")
        cls.leave_confirm = cls._create_leave(data_co)

        # 05-approve.md -- Waiting for Approval record to approve.
        data_ap = cls._create_open_enrollment("AP", "Approve")
        cls.leave_approve = cls._create_leave(data_ap)
        cls.leave_approve.with_user(cls.admin).action_confirm()

        # 06-reject.md -- Waiting for Approval record to reject.
        data_rj = cls._create_open_enrollment("RJ", "Reject")
        cls.leave_reject = cls._create_leave(data_rj)
        cls.leave_reject.with_user(cls.admin).action_confirm()

        # 10-cancel.md -- Waiting for Approval record to cancel.
        data_cn = cls._create_open_enrollment("CN", "Cancel")
        cls.leave_cancel = cls._create_leave(data_cn)
        cls.leave_cancel.with_user(cls.admin).action_confirm()

        # 12-restart.md -- Cancelled record to restart.
        data_rs = cls._create_open_enrollment("RS", "Restart")
        cls.leave_restart = cls._create_leave(data_rs)
        cls.leave_restart.with_user(cls.admin).action_confirm()
        cls.leave_restart.with_user(cls.admin).action_cancel(cls.cancel_reason)

        # 13-reset-number.md -- Draft record with a manually-set
        # document number.
        data_rn = cls._create_open_enrollment("RN", "Reset Number")
        cls.leave_reset_number = cls._create_leave(data_rn)
        cls.leave_reset_number.write({"name": "TOUR-SL-MANUAL-001"})

        # 14-restart-approval.md -- Waiting for Approval record whose
        # approval process is stalled.
        data_ra = cls._create_open_enrollment("RA", "Restart Approval")
        cls.leave_restart_approval = cls._create_leave(data_ra)
        cls.leave_restart_approval.with_user(cls.admin).action_confirm()
        cls.leave_restart_approval.sudo().approval_ids.unlink()
        cls.leave_restart_approval.sudo().write({"approval_template_id": False})

        # 15-return.md -- Done record whose student is currently On
        # Leave.
        data_rt = cls._create_open_enrollment("RT", "Return")
        cls.leave_return = cls._create_leave(data_rt)
        cls.leave_return.with_user(cls.admin).action_confirm()
        cls.leave_return.with_user(cls.admin).action_approve_approval()
        cls.leave_return.invalidate_cache()
        assert cls.leave_return.state == "done"
        data_rt["student"].invalidate_cache()
        assert data_rt["student"].state == "on_leave"

        # 16-print.md -- any state is usable per the IK; a fresh Draft
        # record is enough.
        data_pr = cls._create_open_enrollment("PR", "Print")
        cls.leave_print = cls._create_leave(data_pr)

        # 17-reload-template-policy.md -- any state is usable per the
        # IK; a fresh Draft record is enough.
        data_rp = cls._create_open_enrollment("RP", "Reload Policy")
        cls.leave_reload_template_policy = cls._create_leave(data_rp)

    @classmethod
    def _create_open_enrollment(cls, suffix, label):
        """Build one isolated grade/school/class/year/term/enrollment.

        Brings a new Enrollment to Open status via Confirm + Approve
        (run as ``base.user_admin``, who holds the Validator group so
        the confirm_ok/approve_ok policy fields compute True), which
        also moves the student to the "enrol" state via the
        enrollment's post_open hook.

        :param suffix: short unique code suffix for this fixture set.
        :param label: action label (e.g. "Create", "Edit") used to
            build the tour marker names "TOUR SL <label> Student" /
            "TOUR SL <label> Term", kept in sync with the literals
            used by school_student_leave_tour.js.
        :return: dict with the created records, keyed by role.
        """
        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR SL Grade Type %s" % suffix,
                "code": "GTSL%s" % suffix,
                "sequence": 10,
            }
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR SL School %s" % suffix,
                "code": "SCHSL%s" % suffix,
                "grade_type_id": grade_type.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR SL Grade %s" % suffix,
                "code": "GSL%s" % suffix,
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR SL %s Class" % label,
                "code": "CLSL%s" % suffix,
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR SL Year %s" % suffix,
                "code": "AYSL%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR SL %s Term" % label,
                "code": "TMSL%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        student_name = "TOUR SL %s Student" % label
        contact = cls.env["res.partner"].create({"name": "%s Contact" % student_name})
        student = cls.env["school_student"].create(
            {
                "name": student_name,
                "code": "STUSL%s" % suffix,
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        enrollment = cls.env["school_enrollment"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": year.id,
                "academic_term_id": term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
                "currency_id": cls.env.company.currency_id.id,
            }
        )
        enrollment.with_user(cls.admin).action_confirm()
        enrollment.invalidate_cache()
        enrollment.with_user(cls.admin).action_approve_approval()
        return {
            "school": school,
            "grade": grade,
            "grade_class": grade_class,
            "year": year,
            "term": term,
            "student": student,
            "enrollment": enrollment,
        }

    @classmethod
    def _create_leave(cls, data):
        """Create a Draft leave for the student/term in ``data``.

        :param data: dict returned by ``_create_open_enrollment``.
        :return: the created ``school_student_leave`` record.
        """
        return cls.env["school_student_leave"].create(
            {
                "date": "2024-08-01",
                "student_id": data["student"].id,
                "academic_term_id": data["term"].id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_student_leave``.

        IK: docs/school_student_leave/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_leave_school_student_leave_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_student_leave``.

        IK: docs/school_student_leave/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_leave_school_student_leave_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_student_leave``.

        IK: docs/school_student_leave/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_leave_school_student_leave_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_student_leave``.

        IK: docs/school_student_leave/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_leave_school_student_leave_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_student_leave``.

        IK: docs/school_student_leave/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_leave_school_student_leave_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_student_leave``.

        IK: docs/school_student_leave/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_leave_school_student_leave_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_student_leave``.

        IK: docs/school_student_leave/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_leave_school_student_leave_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``school_student_leave``.

        IK: docs/school_student_leave/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_leave_school_student_leave_restart",
            login="admin",
        )

    def test_reset_number(self):
        """Run the reset document number tour.

        IK: docs/school_student_leave/13-reset-number.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_leave_school_student_leave_reset_number",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval process tour.

        IK: docs/school_student_leave/14-restart-approval.md

        Config Pre-Condition note: policy_template/school_student_
        leave.xml does not ship a policy.template_detail granting
        restart_approval_ok, so this HttpCase's setUpClass supplies
        that detail directly.
        """
        self.start_tour(
            "/web",
            "ssi_school_student_leave_school_student_leave_restart_approval",
            login="admin",
        )

    def test_return(self):
        """Run the return tour for ``school_student_leave``.

        IK: docs/school_student_leave/15-return.md

        Boundary: clicking Return shows no confirmation dialog and does
        not change this document's own status (it stays Done) -- only
        the student's state changes, which is unit test territory. The
        tour only proves the button is reachable, clickable, and the
        form survives the click.
        """
        self.start_tour(
            "/web",
            "ssi_school_student_leave_school_student_leave_return",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_student_leave/16-print.md

        Boundary: the resulting report action is an
        ``ir.actions.act_url`` download with no DOM "finished" signal --
        clicking through it could hang headless Chrome.
        """
        self.start_tour(
            "/web",
            "ssi_school_student_leave_school_student_leave_print",
            login="admin",
        )

    def test_reload_template_policy(self):
        """Run the reload template policy tour.

        IK: docs/school_student_leave/17-reload-template-policy.md

        Boundary: action_reload_policy_template returns nothing and
        triggers no dialog; the tour only proves the button on the
        Policies tab is reachable and clickable, and that the form
        survives the click without error.
        """
        self.start_tour(
            "/web",
            ("ssi_school_student_leave_school_student_leave_" "reload_template_policy"),
            login="admin",
        )
