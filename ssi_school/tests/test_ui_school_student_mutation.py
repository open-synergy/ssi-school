# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolStudentMutation(HttpSavepointCase):
    """Tour tests for the ``school_student_mutation`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create every Pre-Condition fixture required by the 12 tours.

        Each tour gets its own isolated grade type / school / grade /
        pair (or trio) of grade classes / academic year & term / student
        / open enrollment, built via ``_create_open_enrollment``, so
        that state-changing tours (confirm, approve, reject, cancel,
        restart, ...) never interfere with each other's data.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Config Pre-Condition shared by 10-cancel.md: a cancel reason
        # usable on any model.
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR SM Cancel Reason",
                "code": "TOUR-SM-CANCEL",
                "global_use": True,
            }
        )

        # Config Pre-Condition for 15-print.md: a print_document_type
        # linking a report to school_student_mutation, so the "Select
        # Report To Print" wizard has a report to offer. The tour itself
        # never selects nor prints the report (see test_print
        # docstring), so this report action is a placeholder that is
        # never rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Student Class Mutation Report",
                "model": "school_student_mutation",
                "report_type": "qweb-pdf",
                "report_name": ("ssi_school.tour_school_student_mutation_report"),
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR SM Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_student_mutation"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )

        # Config Pre-Condition for 14-restart-approval.md: the IK
        # itself states that an active policy.template must grant
        # restart_approval_ok for state "confirm" to the actor's
        # group, but policy_template/school_student_mutation.xml does
        # not ship that policy.template_detail (verified: no module
        # data file in ssi_school grants restart_approval_ok for this
        # model). Without it, restart_approval_ok always defaults to
        # False (ssi_policy_mixin._prepare_policy_field_data leaves
        # any policy field with no matching detail at False) and the
        # "Restart Approval Process" button never renders. This is
        # exactly the class of Config Pre-Condition the IK documents
        # but the module does not ship by default, so it is supplied
        # here as HttpCase setup data -- mirroring the declarative
        # shape of the other <field>_ok details already shipped in
        # policy_template/school_student_mutation.xml. The IK's Actor
        # for this button is "User" (not "Validator"), so the group
        # granted is school_student_mutation_user_group, matching the
        # confirm_ok detail in that same file rather than the
        # Validator-gated ones (cancel_ok, restart_ok,
        # manual_number_ok).
        policy_template = cls.env.ref(
            "ssi_school.policy_template_school_student_mutation"
        )
        state_field = cls.env["ir.model.fields"].search(
            [
                ("model_id.model", "=", "school_student_mutation"),
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
                ("model_id.model", "=", "school_student_mutation"),
                ("name", "=", "restart_approval_ok"),
            ],
            limit=1,
        )
        user_group = cls.env.ref("ssi_school.school_student_mutation_user_group")
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

        # 01-create.md -- no mutation record is pre-created; the create
        # tour creates a new one. It still needs a student with an open
        # Enrollment to pick from the list, and a second Grade Class
        # (destination) in the same Grade/School.
        cls._create_open_enrollment("CR", "Create")

        # 02-edit.md -- Draft record to edit, plus a third Grade Class
        # so the tour can switch the Destination Grade Class to it.
        data_ed = cls._create_open_enrollment("ED", "Edit")
        cls.grade_class_ed_c = cls.env["school_grade_class"].create(
            {
                "name": "TOUR SM Edit Class C",
                "code": "CLSMEDC",
                "school_id": data_ed["school"].id,
                "grade_id": data_ed["grade"].id,
                "capacity": 30,
            }
        )
        cls.mutation_edit = cls._create_mutation(data_ed)

        # 03-delete.md -- Draft record to delete.
        data_dl = cls._create_open_enrollment("DL", "Delete")
        cls.mutation_delete = cls._create_mutation(data_dl)

        # 04-confirm.md -- Draft record to confirm.
        data_co = cls._create_open_enrollment("CO", "Confirm")
        cls.mutation_confirm = cls._create_mutation(data_co)

        # 05-approve.md -- Waiting for Approval record to approve.
        data_ap = cls._create_open_enrollment("AP", "Approve")
        cls.mutation_approve = cls._create_mutation(data_ap)
        cls.mutation_approve.with_user(cls.admin).action_confirm()

        # 06-reject.md -- Waiting for Approval record to reject.
        data_rj = cls._create_open_enrollment("RJ", "Reject")
        cls.mutation_reject = cls._create_mutation(data_rj)
        cls.mutation_reject.with_user(cls.admin).action_confirm()

        # 10-cancel.md -- Waiting for Approval record to cancel.
        data_cn = cls._create_open_enrollment("CN", "Cancel")
        cls.mutation_cancel = cls._create_mutation(data_cn)
        cls.mutation_cancel.with_user(cls.admin).action_confirm()

        # 12-restart.md -- Cancelled record to restart.
        data_rs = cls._create_open_enrollment("RS", "Restart")
        cls.mutation_restart = cls._create_mutation(data_rs)
        cls.mutation_restart.with_user(cls.admin).action_confirm()
        cls.mutation_restart.with_user(cls.admin).action_cancel(cls.cancel_reason)

        # 13-reset-number.md -- Draft record with a manually-set
        # document number (the "name" field is editable in Draft
        # status).
        data_rn = cls._create_open_enrollment("RN", "Reset Number")
        cls.mutation_reset_number = cls._create_mutation(data_rn)
        cls.mutation_reset_number.write({"name": "TOUR-SM-MANUAL-001"})

        # 14-restart-approval.md -- Waiting for Approval record whose
        # approval process is stalled (no approval template assigned,
        # existing approval records discarded), matching the IK's
        # Pre-Condition literally. The restart_approval_ok policy
        # detail created above supplies the Config Pre-Condition the
        # IK requires, so the "Restart Approval Process" button
        # renders for this record.
        data_ra = cls._create_open_enrollment("RA", "Restart Approval")
        cls.mutation_restart_approval = cls._create_mutation(data_ra)
        cls.mutation_restart_approval.with_user(cls.admin).action_confirm()
        cls.mutation_restart_approval.sudo().approval_ids.unlink()
        cls.mutation_restart_approval.sudo().write({"approval_template_id": False})

        # 15-print.md -- any state is usable per the IK; a fresh Draft
        # record is enough.
        data_pr = cls._create_open_enrollment("PR", "Print")
        cls.mutation_print = cls._create_mutation(data_pr)

        # 16-reload-template-policy.md -- any state is usable per the
        # IK; a fresh Draft record is enough.
        data_rt = cls._create_open_enrollment("RT", "Reload Policy")
        cls.mutation_reload_template_policy = cls._create_mutation(data_rt)

    @classmethod
    def _create_open_enrollment(cls, suffix, label):
        """Build one isolated grade/school/class/year/term/enrollment.

        Mirrors ``TestSchoolStudentMutation._setup_open_enrollment`` in
        ``tests/test_school_student_mutation.py``: creates its own
        Grade Type, School, Grade, two Grade Classes (A = source, B =
        destination), Academic Year/Term, and Student, then brings a
        new Enrollment to Open status via Confirm + Approve (run as
        ``base.user_admin``, who holds the Validator group so the
        confirm_ok/approve_ok policy fields compute True).

        :param suffix: short unique code suffix for this fixture set.
        :param label: action label (e.g. "Create", "Edit") used to
            build the tour marker names "TOUR SM <label> Student" /
            "... Class A" / "... Class B", kept in sync with the
            literals used by school_student_mutation_tour.js.
        :return: dict with the created records, keyed by role.
        """
        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR SM Grade Type %s" % suffix,
                "code": "GTSM%s" % suffix,
                "sequence": 10,
            }
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR SM School %s" % suffix,
                "code": "SCHSM%s" % suffix,
                "grade_type_id": grade_type.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR SM Grade %s" % suffix,
                "code": "GSM%s" % suffix,
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class_a = cls.env["school_grade_class"].create(
            {
                "name": "TOUR SM %s Class A" % label,
                "code": "CLSM%sA" % suffix,
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        grade_class_b = cls.env["school_grade_class"].create(
            {
                "name": "TOUR SM %s Class B" % label,
                "code": "CLSM%sB" % suffix,
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR SM Year %s" % suffix,
                "code": "AYSM%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR SM Term %s" % suffix,
                "code": "TMSM%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        student_name = "TOUR SM %s Student" % label
        contact = cls.env["res.partner"].create({"name": "%s Contact" % student_name})
        student = cls.env["school_student"].create(
            {
                "name": student_name,
                "code": "STUSM%s" % suffix,
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
                "grade_class_id": grade_class_a.id,
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
            "grade_class_a": grade_class_a,
            "grade_class_b": grade_class_b,
            "student": student,
            "enrollment": enrollment,
        }

    @classmethod
    def _create_mutation(cls, data):
        """Create a Draft mutation from Class A to Class B for ``data``.

        :param data: dict returned by ``_create_open_enrollment``.
        :return: the created ``school_student_mutation`` record.
        """
        return cls.env["school_student_mutation"].create(
            {
                "date": "2024-07-01",
                "student_id": data["student"].id,
                "enrollment_id": data["enrollment"].id,
                "destination_grade_class_id": data["grade_class_b"].id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_student_mutation``.

        IK: docs/school_student_mutation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_mutation_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_student_mutation``.

        IK: docs/school_student_mutation/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_mutation_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_student_mutation``.

        IK: docs/school_student_mutation/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_mutation_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_student_mutation``.

        IK: docs/school_student_mutation/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_mutation_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_student_mutation``.

        IK: docs/school_student_mutation/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_mutation_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_student_mutation``.

        IK: docs/school_student_mutation/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_mutation_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_student_mutation``.

        IK: docs/school_student_mutation/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_mutation_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``school_student_mutation``.

        IK: docs/school_student_mutation/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_mutation_restart",
            login="admin",
        )

    def test_reset_number(self):
        """Run the reset document number tour.

        IK: docs/school_student_mutation/13-reset-number.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_mutation_reset_number",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval process tour.

        IK: docs/school_student_mutation/14-restart-approval.md

        Config Pre-Condition note: policy_template/school_student_
        mutation.xml does not ship a policy.template_detail granting
        restart_approval_ok, so this HttpCase's setUpClass supplies
        that detail directly (as the IK's own Config Pre-Condition
        requires), mirroring the declarative shape of the details
        already shipped in that file. Without it the "Restart
        Approval Process" button would never render for any user.
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_mutation_restart_approval",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_student_mutation/15-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_mutation_print",
            login="admin",
        )

    def test_reload_template_policy(self):
        """Run the reload template policy tour.

        IK: docs/school_student_mutation/16-reload-template-policy.md

        Boundary: action_reload_policy_template returns nothing and
        triggers no dialog, so the tour only proves the button on the
        Policies tab is reachable and clickable, and that the form
        survives the click without error. The actual template
        re-assignment is unit test territory.
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_mutation_reload_template_policy",
            login="admin",
        )
