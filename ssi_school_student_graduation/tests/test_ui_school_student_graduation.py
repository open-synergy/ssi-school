# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolStudentGraduation(HttpSavepointCase):
    """Tour tests for the ``school_student_graduation`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create every Pre-Condition fixture required by the 12 tours.

        Each tour gets its own isolated grade type / school / grade /
        grade class / academic year & term / student, brought to the
        Enrolled state via ``_create_open_enrollment``, so
        state-changing tours (confirm, approve, reject, cancel,
        restart, ...) never interfere with each other's data.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Config Pre-Condition shared by 10-cancel.md: a cancel reason
        # usable on any model.
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR SG Cancel Reason",
                "code": "TOUR-SG-CANCEL",
                "global_use": True,
            }
        )

        # Config Pre-Condition for 15-print.md: a print_document_type
        # linking a report to school_student_graduation, so the
        # "Select Report To Print" wizard has a report to offer. The
        # tour itself never selects nor prints the report (see
        # test_print docstring), so this report action is a
        # placeholder that is never rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Student Graduation Report",
                "model": "school_student_graduation",
                "report_type": "qweb-pdf",
                "report_name": (
                    "ssi_school_student_graduation."
                    "tour_school_student_graduation_report"
                ),
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR SG Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_student_graduation"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )

        # Config Pre-Condition for 14-restart-approval.md: the IK
        # itself states that an active policy.template must grant
        # restart_approval_ok for state "confirm" to the actor's
        # group, but policy_template/school_student_graduation.xml
        # does not ship that policy.template_detail (verified: no
        # module data file in ssi_school_student_graduation grants
        # restart_approval_ok for this model). Without it,
        # restart_approval_ok always defaults to False
        # (ssi_policy_mixin._prepare_policy_field_data leaves any
        # policy field with no matching detail at False) and the
        # "Restart Approval Process" button never renders. This is
        # exactly the class of Config Pre-Condition the IK documents
        # but the module does not ship by default, so it is supplied
        # here as HttpCase setup data -- mirroring the declarative
        # shape of the other <field>_ok details already shipped in
        # policy_template/school_student_graduation.xml. The IK's
        # Actor for this button is "User" (not "Validator"), so the
        # group granted is school_student_graduation_user_group,
        # matching the confirm_ok detail in that same file rather than
        # the Validator-gated ones (cancel_ok, restart_ok,
        # manual_number_ok).
        policy_template = cls.env.ref(
            "ssi_school_student_graduation.policy_template_school_student_graduation"
        )
        state_field = cls.env["ir.model.fields"].search(
            [
                ("model_id.model", "=", "school_student_graduation"),
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
                ("model_id.model", "=", "school_student_graduation"),
                ("name", "=", "restart_approval_ok"),
            ],
            limit=1,
        )
        user_group = cls.env.ref(
            "ssi_school_student_graduation.school_student_graduation_user_group"
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

        # 01-create.md -- no graduation record is pre-created; the
        # create tour creates a new one. It only needs an Enrolled
        # student to pick from the list.
        cls._create_open_enrollment("CR", "Create")

        # 02-edit.md -- Draft record on an initial student, plus a
        # second Enrolled student the tour reassigns the record to.
        data_ed = cls._create_open_enrollment("ED", "Edit")
        cls._create_open_enrollment("EDT", "Edit Target")
        cls.graduation_edit = cls._create_graduation(data_ed)

        # 03-delete.md -- Draft record to delete.
        data_dl = cls._create_open_enrollment("DL", "Delete")
        cls.graduation_delete = cls._create_graduation(data_dl)

        # 04-confirm.md -- Draft record to confirm.
        data_co = cls._create_open_enrollment("CO", "Confirm")
        cls.graduation_confirm = cls._create_graduation(data_co)

        # 05-approve.md -- Waiting for Approval record to approve.
        data_ap = cls._create_open_enrollment("AP", "Approve")
        cls.graduation_approve = cls._create_graduation(data_ap)
        cls.graduation_approve.with_user(cls.admin).action_confirm()

        # 06-reject.md -- Waiting for Approval record to reject.
        data_rj = cls._create_open_enrollment("RJ", "Reject")
        cls.graduation_reject = cls._create_graduation(data_rj)
        cls.graduation_reject.with_user(cls.admin).action_confirm()

        # 10-cancel.md -- Waiting for Approval record to cancel.
        data_cn = cls._create_open_enrollment("CN", "Cancel")
        cls.graduation_cancel = cls._create_graduation(data_cn)
        cls.graduation_cancel.with_user(cls.admin).action_confirm()

        # 12-restart.md -- Cancelled record to restart.
        data_rs = cls._create_open_enrollment("RS", "Restart")
        cls.graduation_restart = cls._create_graduation(data_rs)
        cls.graduation_restart.with_user(cls.admin).action_confirm()
        cls.graduation_restart.with_user(cls.admin).action_cancel(cls.cancel_reason)

        # 13-reset-number.md -- Draft record with a manually-set
        # document number (the "name" field is editable in Draft
        # status).
        data_rn = cls._create_open_enrollment("RN", "Reset Number")
        cls.graduation_reset_number = cls._create_graduation(data_rn)
        cls.graduation_reset_number.write({"name": "TOUR-SG-MANUAL-001"})

        # 14-restart-approval.md -- Waiting for Approval record whose
        # approval process is stalled (no approval template assigned,
        # existing approval records discarded), matching the IK's
        # Pre-Condition literally. The restart_approval_ok policy
        # detail created above supplies the Config Pre-Condition the
        # IK requires, so the "Restart Approval Process" button
        # renders for this record.
        data_ra = cls._create_open_enrollment("RA", "Restart Approval")
        cls.graduation_restart_approval = cls._create_graduation(data_ra)
        cls.graduation_restart_approval.with_user(cls.admin).action_confirm()
        cls.graduation_restart_approval.sudo().approval_ids.unlink()
        cls.graduation_restart_approval.sudo().write({"approval_template_id": False})

        # 15-print.md -- any state is usable per the IK; a fresh Draft
        # record is enough.
        data_pr = cls._create_open_enrollment("PR", "Print")
        cls.graduation_print = cls._create_graduation(data_pr)

        # 16-reload-template-policy.md -- any state is usable per the
        # IK; a fresh Draft record is enough.
        data_rt = cls._create_open_enrollment("RT", "Reload Policy")
        cls.graduation_reload_template_policy = cls._create_graduation(data_rt)

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
            build the tour marker name "TOUR SG <label> Student",
            kept in sync with the literals used by
            school_student_graduation_tour.js.
        :return: dict with the created records, keyed by role.
        """
        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR SG Grade Type %s" % suffix,
                "code": "GTSG%s" % suffix,
                "sequence": 10,
            }
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR SG School %s" % suffix,
                "code": "SCHSG%s" % suffix,
                "grade_type_id": grade_type.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR SG Grade %s" % suffix,
                "code": "GSG%s" % suffix,
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR SG %s Class" % label,
                "code": "CLSG%s" % suffix,
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR SG Year %s" % suffix,
                "code": "AYSG%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR SG Term %s" % suffix,
                "code": "TMSG%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        student_name = "TOUR SG %s Student" % label
        contact = cls.env["res.partner"].create({"name": "%s Contact" % student_name})
        student = cls.env["school_student"].create(
            {
                "name": student_name,
                "code": "STUSG%s" % suffix,
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
            "student": student,
            "enrollment": enrollment,
        }

    @classmethod
    def _create_graduation(cls, data):
        """Create a Draft graduation for the student in ``data``.

        ``user_id`` is set explicitly to ``base.user_admin`` -- without
        it, ``mixin.transaction._default_user_id`` defaults new
        records to the superuser (``SavepointCase.setUpClass`` runs as
        ``SUPERUSER_ID``), and the internal-user record rule
        ``[('user_id', '=', user.id)]`` then hides the fixture from
        the tour's "admin" session, so the list shows zero rows with
        no error (verified in issue #227 / PR #250).

        :param data: dict returned by ``_create_open_enrollment``.
        :return: the created ``school_student_graduation`` record.
        """
        return cls.env["school_student_graduation"].create(
            {
                "date": "2025-06-30",
                "student_id": data["student"].id,
                "graduation_date": "2025-06-30",
                "user_id": cls.admin.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_student_graduation``.

        IK: docs/school_student_graduation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_student_graduation``.

        IK: docs/school_student_graduation/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_student_graduation``.

        IK: docs/school_student_graduation/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_student_graduation``.

        IK: docs/school_student_graduation/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_student_graduation``.

        IK: docs/school_student_graduation/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_student_graduation``.

        IK: docs/school_student_graduation/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_student_graduation``.

        IK: docs/school_student_graduation/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``school_student_graduation``.

        IK: docs/school_student_graduation/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_restart",
            login="admin",
        )

    def test_reset_number(self):
        """Run the reset document number tour.

        IK: docs/school_student_graduation/13-reset-number.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_reset_number",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval process tour.

        IK: docs/school_student_graduation/14-restart-approval.md

        Config Pre-Condition note: policy_template/school_student_
        graduation.xml does not ship a policy.template_detail granting
        restart_approval_ok, so this HttpCase's setUpClass supplies
        that detail directly (as the IK's own Config Pre-Condition
        requires), mirroring the declarative shape of the details
        already shipped in that file. Without it the "Restart
        Approval Process" button would never render for any user.
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_restart_approval",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_student_graduation/15-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_print",
            login="admin",
        )

    def test_reload_template_policy(self):
        """Run the reload template policy tour.

        IK: docs/school_student_graduation/16-reload-template-policy.md

        Boundary: action_reload_policy_template returns nothing and
        triggers no dialog, so the tour only proves the button on the
        Policies tab is reachable and clickable, and that the form
        survives the click without error. The actual template
        re-assignment is unit test territory.
        """
        self.start_tour(
            "/web",
            (
                "ssi_school_student_graduation_school_student_graduation_"
                "reload_template_policy"
            ),
            login="admin",
        )
