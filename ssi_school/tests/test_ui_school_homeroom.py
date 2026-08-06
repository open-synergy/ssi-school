# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolHomeroom(HttpSavepointCase):
    """UI/UX tour tests for ``school_homeroom``.

    Every ``test_*`` method below runs the tour pairing with the IK file
    named in its docstring (``docs/school_homeroom/NN-*.md``). All
    Pre-Condition data is prepared here in Python -- never through UI
    steps -- following the tour authoring doctrine: prerequisite data
    belongs to ``setUpClass``, the tour itself only exercises the
    click-flow documented in the IK. ``school_homeroom_validator_group``
    already includes ``base.user_admin`` by default
    (``security/res_group/school_homeroom.xml``), which implies both
    ``school_homeroom_user_group`` and ``school_homeroom_viewer_group``,
    so no extra group grant is needed for any tour here.
    """

    @classmethod
    def setUpClass(cls):
        """Create the reference data and Homeroom fixtures the tours use.

        A single Grade Type / School / Grade / Academic Year is shared by
        every fixture below. Two Academic Terms are created under that
        year: ``term_1`` (Jul-Dec, automatically the first term of the
        year) used by fixtures that do not exercise student eligibility,
        and ``term_2`` (Jan-Jun, non-first) used by the Fill Random and
        Generate Enrollments fixtures, whose eligible students are given
        ``initial_grade_id`` equal to the target Grade so that
        ``current_grade_id`` (the criterion used on non-first terms)
        matches directly. Each Homeroom fixture gets its own dedicated
        Grade Class, whose unique name is also the marker the tours use
        to find the right row in the Homerooms list (the document number
        of a Draft record is still "/", so it cannot be used as a
        marker).
        """
        super().setUpClass()

        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR HR Grade Type",
                "code": "/",
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR HR School",
                "code": "/",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "TOUR HR Grade",
                "code": "/",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR HR Academic Year",
                "code": "/",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.term_1 = cls.env["school_academic_term"].create(
            {
                "name": "TOUR HR Term 1",
                "code": "/",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.academic_year.id,
            }
        )
        cls.term_2 = cls.env["school_academic_term"].create(
            {
                "name": "TOUR HR Term 2",
                "code": "/",
                "date_start": "2025-01-01",
                "date_end": "2025-06-30",
                "year_id": cls.academic_year.id,
            }
        )

        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR HR Cancel Reason",
                "code": "TOUR-HR-CANCEL",
                "global_use": True,
            }
        )

        # Config Pre-Condition for docs/school_homeroom/14-restart-approval.md:
        # the module's default policy.template (policy_template_school_
        # homeroom) has no detail granting restart_approval_ok -- without
        # one, the field always computes False and the button never
        # renders. Add the missing detail the same way the module itself
        # declares its other policy.template_detail records.
        confirm_state = cls.env["ir.model.fields.selection"].search(
            [
                ("field_id.model_id.model", "=", "school_homeroom"),
                ("field_id.name", "=", "state"),
                ("value", "=", "confirm"),
            ]
        )
        cls.env["policy.template_detail"].create(
            {
                "template_id": cls.env.ref(
                    "ssi_school.policy_template_school_homeroom"
                ).id,
                "field_id": cls.env["ir.model.fields"]
                ._get("school_homeroom", "restart_approval_ok")
                .id,
                "restrict_state": True,
                "state_ids": [(6, 0, confirm_state.ids)],
                "restrict_user": True,
                "computation_method": "use_group",
                "group_ids": [
                    (6, 0, [cls.env.ref("ssi_school.school_homeroom_user_group").id])
                ],
                "restrict_additional": False,
            }
        )

        # Pre-Condition for docs/school_homeroom/01-create.md: a Grade
        # Class the tour itself picks from the many2one dropdown. No
        # Homeroom fixture is created for it -- the create tour creates
        # the record.
        cls.grade_class_create = cls._create_grade_class("TOUR HR CREATE CLASS")

        # Pre-Condition for docs/school_homeroom/02-edit.md: a Draft
        # record to edit, plus a second Grade Class to switch to.
        cls.grade_class_edit = cls._create_grade_class("TOUR HR EDIT CLASS")
        cls.grade_class_edit_b = cls._create_grade_class("TOUR HR EDIT CLASS B")
        cls.homeroom_edit = cls._create_homeroom(cls.grade_class_edit)

        # Pre-Condition for docs/school_homeroom/03-delete.md: a Draft
        # record whose document number is still "/".
        cls.grade_class_delete = cls._create_grade_class("TOUR HR DELETE CLASS")
        cls.homeroom_delete = cls._create_homeroom(cls.grade_class_delete)

        # Pre-Condition for docs/school_homeroom/04-confirm.md: a Draft
        # record to confirm.
        cls.grade_class_confirm = cls._create_grade_class("TOUR HR CONFIRM CLASS")
        cls.homeroom_confirm = cls._create_homeroom(cls.grade_class_confirm)

        # Pre-Condition for docs/school_homeroom/05-approve.md: a Waiting
        # for Approval record to approve.
        cls.grade_class_approve = cls._create_grade_class("TOUR HR APPROVE CLASS")
        cls.homeroom_approve = cls._create_homeroom(cls.grade_class_approve)
        cls.homeroom_approve.action_confirm()

        # Pre-Condition for docs/school_homeroom/06-reject.md: a Waiting
        # for Approval record to reject.
        cls.grade_class_reject = cls._create_grade_class("TOUR HR REJECT CLASS")
        cls.homeroom_reject = cls._create_homeroom(cls.grade_class_reject)
        cls.homeroom_reject.action_confirm()

        # Pre-Condition for docs/school_homeroom/09-finish.md: an On
        # Progress record to finish. The single-level approval template
        # (school_homeroom_validator_group, which admin belongs to)
        # fulfills on the first approval, auto-transitioning to Open.
        cls.grade_class_finish = cls._create_grade_class("TOUR HR FINISH CLASS")
        cls.homeroom_finish = cls._create_homeroom(cls.grade_class_finish)
        cls.homeroom_finish.action_confirm()
        cls.homeroom_finish.action_approve_approval()

        # Pre-Condition for docs/school_homeroom/10-cancel.md: a Draft
        # record to cancel.
        cls.grade_class_cancel = cls._create_grade_class("TOUR HR CANCEL CLASS")
        cls.homeroom_cancel = cls._create_homeroom(cls.grade_class_cancel)

        # Pre-Condition for docs/school_homeroom/12-restart.md: a
        # Cancelled record to restart.
        cls.grade_class_restart = cls._create_grade_class("TOUR HR RESTART CLASS")
        cls.homeroom_restart = cls._create_homeroom(cls.grade_class_restart)
        cls.homeroom_restart.action_confirm()
        cls.homeroom_restart.action_cancel(cls.cancel_reason)

        # Pre-Condition for docs/school_homeroom/13-reset-number.md: a
        # Draft record with a manually-set document number (the "name"
        # field is editable in Draft status).
        cls.grade_class_reset_number = cls._create_grade_class(
            "TOUR HR RESET NUMBER CLASS"
        )
        cls.homeroom_reset_number = cls._create_homeroom(cls.grade_class_reset_number)
        cls.homeroom_reset_number.write({"name": "TOUR-HR-MANUAL-001"})

        # Pre-Condition for docs/school_homeroom/14-restart-approval.md: a
        # Waiting for Approval record, with the policy.template_detail
        # created above granting restart_approval_ok.
        cls.grade_class_restart_approval = cls._create_grade_class(
            "TOUR HR RESTART APPROVAL CLASS"
        )
        cls.homeroom_restart_approval = cls._create_homeroom(
            cls.grade_class_restart_approval
        )
        cls.homeroom_restart_approval.action_confirm()

        # Pre-Condition for docs/school_homeroom/15-fill-random.md: a
        # Draft record on term_2 (non-first term) with Capacity 1 and
        # exactly one Draft student eligible for that Grade/Term/School
        # and not yet a candidate -- this makes the outcome of "random"
        # selection deterministic (the pool has only one member).
        cls.grade_class_fill_random = cls._create_grade_class(
            "TOUR HR FILL RANDOM CLASS"
        )
        cls.homeroom_fill_random = cls._create_homeroom(
            cls.grade_class_fill_random, term=cls.term_2, capacity=1
        )
        cls.student_fill_random = cls._create_student("TOUR HR FILL RANDOM STUDENT")

        # Pre-Condition for docs/school_homeroom/16-generate-enrollments.md:
        # an On Progress record on term_2 whose Candidate Students already
        # contains one eligible student without an Enrollment yet -- the
        # tour only proves the button can be clicked to completion (see
        # test_generate_enrollments docstring for the async-job boundary).
        cls.grade_class_generate = cls._create_grade_class("TOUR HR GENERATE CLASS")
        cls.student_generate = cls._create_student("TOUR HR GENERATE STUDENT")
        cls.homeroom_generate = cls._create_homeroom(
            cls.grade_class_generate,
            term=cls.term_2,
            capacity=5,
            candidate_students=cls.student_generate,
        )
        cls.homeroom_generate.action_confirm()
        cls.homeroom_generate.action_approve_approval()

        # Pre-Condition for docs/school_homeroom/17-print.md: a
        # print_document_type linking a report to `school_homeroom` is
        # required for the wizard to have a report to offer -- without it
        # the wizard still opens but the report list is empty. The tour
        # itself never selects nor prints the report (see test_print
        # docstring), so the report action is a placeholder that is
        # never rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR HR Report",
                "model": "school_homeroom",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school.tour_school_homeroom_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR HR Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_homeroom"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.grade_class_print = cls._create_grade_class("TOUR HR PRINT CLASS")
        cls.homeroom_print = cls._create_homeroom(cls.grade_class_print)

        # Pre-Condition for docs/school_homeroom/18-reload-template-
        # policy.md: any record works, since action_reload_policy_template
        # is not gated by state -- the button is only gated by the
        # base.group_system group on the view, and admin already belongs
        # to it by default.
        cls.grade_class_reload_policy = cls._create_grade_class(
            "TOUR HR RELOAD POLICY CLASS"
        )
        cls.homeroom_reload_policy = cls._create_homeroom(cls.grade_class_reload_policy)

    @classmethod
    def _create_grade_class(cls, name):
        """Create a Grade Class under the shared School/Grade fixtures."""
        return cls.env["school_grade_class"].create(
            {
                "name": name,
                "code": "/",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "capacity": 10,
            }
        )

    @classmethod
    def _create_homeroom(
        cls, grade_class, term=None, capacity=10, candidate_students=None
    ):
        """Create a Draft Homeroom for the given Grade Class.

        Uses ``term_1`` by default -- eligibility is only exercised by
        the Fill Random and Generate Enrollments fixtures, which pass
        ``term_2`` explicitly.
        """
        values = {
            "date": "2024-07-01",
            "academic_year_id": cls.academic_year.id,
            "academic_term_id": (term or cls.term_1).id,
            "school_id": cls.school.id,
            "grade_id": cls.grade.id,
            "grade_class_id": grade_class.id,
            "capacity": capacity,
        }
        if candidate_students is not None:
            values["candidate_student_ids"] = [(6, 0, candidate_students.ids)]
        return cls.env["school_homeroom"].create(values)

    @classmethod
    def _create_student(cls, name):
        """Create a Draft student eligible for the shared School/Grade.

        ``initial_grade_id`` is set to the shared Grade directly, so on
        the non-first ``term_2`` (which matches on ``current_grade_id``,
        equal to ``initial_grade_id`` when there is no enrollment
        history yet) the student is eligible without needing a second,
        "previous" Grade.
        """
        contact = cls.env["res.partner"].create({"name": "Contact %s" % name})
        return cls.env["school_student"].create(
            {
                "name": name,
                "code": "/",
                "contact_id": contact.id,
                "school_id": cls.school.id,
                "initial_grade_id": cls.grade.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_homeroom``.

        IK: docs/school_homeroom/01-create.md
        """
        self.start_tour("/web", "ssi_school_school_homeroom_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``school_homeroom``.

        IK: docs/school_homeroom/02-edit.md
        """
        self.start_tour("/web", "ssi_school_school_homeroom_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``school_homeroom``.

        IK: docs/school_homeroom/03-delete.md
        """
        self.start_tour("/web", "ssi_school_school_homeroom_delete", login="admin")

    def test_confirm(self):
        """Run the confirm tour for ``school_homeroom``.

        IK: docs/school_homeroom/04-confirm.md
        """
        self.start_tour("/web", "ssi_school_school_homeroom_confirm", login="admin")

    def test_approve(self):
        """Run the approve tour for ``school_homeroom``.

        IK: docs/school_homeroom/05-approve.md
        """
        self.start_tour("/web", "ssi_school_school_homeroom_approve", login="admin")

    def test_reject(self):
        """Run the reject tour for ``school_homeroom``.

        IK: docs/school_homeroom/06-reject.md
        """
        self.start_tour("/web", "ssi_school_school_homeroom_reject", login="admin")

    def test_finish(self):
        """Run the finish tour for ``school_homeroom``.

        IK: docs/school_homeroom/09-finish.md
        """
        self.start_tour("/web", "ssi_school_school_homeroom_finish", login="admin")

    def test_cancel(self):
        """Run the cancel tour for ``school_homeroom``.

        IK: docs/school_homeroom/10-cancel.md
        """
        self.start_tour("/web", "ssi_school_school_homeroom_cancel", login="admin")

    def test_restart(self):
        """Run the restart tour for ``school_homeroom``.

        IK: docs/school_homeroom/12-restart.md
        """
        self.start_tour("/web", "ssi_school_school_homeroom_restart", login="admin")

    def test_reset_number(self):
        """Run the reset document number tour for ``school_homeroom``.

        IK: docs/school_homeroom/13-reset-number.md
        """
        self.start_tour(
            "/web", "ssi_school_school_homeroom_reset_number", login="admin"
        )

    def test_restart_approval(self):
        """Run the restart approval process tour for ``school_homeroom``.

        IK: docs/school_homeroom/14-restart-approval.md
        """
        self.start_tour(
            "/web", "ssi_school_school_homeroom_restart_approval", login="admin"
        )

    def test_fill_random(self):
        """Run the Fill Random tour for ``school_homeroom``.

        IK: docs/school_homeroom/15-fill-random.md
        """
        self.start_tour("/web", "ssi_school_school_homeroom_fill_random", login="admin")

    def test_generate_enrollments(self):
        """Click Generate Enrollments and confirm the dialog, no more.

        IK: docs/school_homeroom/16-generate-enrollments.md

        Boundary: ``action_generate_enrollments`` enqueues one
        ``queue.job`` per new candidate via ``with_delay()`` to actually
        create the ``school_enrollment`` records (see
        ``_enqueue_generate`` in ``models/school_homeroom.py``). Under
        ``HttpSavepointCase`` the whole test runs inside one rolled-back
        savepoint, so a queue job runner never gets a committed job to
        pick up -- the created Enrollment can never be observed here.
        The tour therefore only proves the click-through completes (the
        confirmation dialog appears, the RPC round-trips, and the record
        stays On Progress with no error), matching patterns.md §Q/§P;
        asserting the resulting Enrollment row is unit test territory.
        """
        self.start_tour(
            "/web", "ssi_school_school_homeroom_generate_enrollments", login="admin"
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_homeroom/17-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour("/web", "ssi_school_school_homeroom_print", login="admin")

    def test_reload_template_policy(self):
        """Assert the Reload Template Policy button on the Policies tab.

        IK: docs/school_homeroom/18-reload-template-policy.md

        Boundary: the tour only proves the Policies tab renders the
        button (gated by ``base.group_system``) and that clicking it
        leaves the tab displayed with no error raised. The resulting
        ``policy_template_id`` value, and the dependent ``*_ok`` fields
        it recomputes, are never asserted here -- that is unit test
        territory.
        """
        self.start_tour(
            "/web",
            "ssi_school_school_homeroom_reload_template_policy",
            login="admin",
        )
