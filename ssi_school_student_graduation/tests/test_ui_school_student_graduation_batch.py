# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolStudentGraduationBatch(HttpSavepointCase):
    """Tour tests for the ``school_student_graduation_batch`` IK."""

    @classmethod
    def setUpClass(cls):
        """Create every Pre-Condition fixture required by the 12 tours.

        Each state-changing tour (confirm, approve, reject, cancel,
        restart, ...) gets its own batch record, marked by a
        uniquely-named Academic Year set on ``academic_year_id`` (used
        as the list-row search marker, since the batch itself has no
        free-text field of its own), plus one manually-added line so
        the "at least one student line exists" Pre-Condition holds.
        The create/edit tours instead rely on freshly-created eligible
        students (Enrolled, no Next Grade) that the Populate Eligible
        Students inline action discovers at runtime.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Config Pre-Condition shared by 10-cancel.md: a cancel reason
        # usable on any model.
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR SGB Cancel Reason",
                "code": "TOUR-SGB-CANCEL",
                "global_use": True,
            }
        )

        # Config Pre-Condition for 15-print.md.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Student Graduation Batch Report",
                "model": "school_student_graduation_batch",
                "report_type": "qweb-pdf",
                "report_name": (
                    "ssi_school_student_graduation."
                    "tour_school_student_graduation_batch_report"
                ),
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR SGB Print Type",
                "model_id": cls.env["ir.model"]._get_id(
                    "school_student_graduation_batch"
                ),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )

        # Config Pre-Condition for 14-restart-approval.md -- same
        # reasoning as TestUiSchoolStudentGraduation.setUpClass:
        # policy_template/school_student_graduation_batch.xml does not
        # ship a policy.template_detail granting restart_approval_ok,
        # so it is supplied here directly.
        policy_template = cls.env.ref(
            "ssi_school_student_graduation."
            "policy_template_school_student_graduation_batch"
        )
        state_field = cls.env["ir.model.fields"].search(
            [
                ("model_id.model", "=", "school_student_graduation_batch"),
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
                ("model_id.model", "=", "school_student_graduation_batch"),
                ("name", "=", "restart_approval_ok"),
            ],
            limit=1,
        )
        user_group = cls.env.ref(
            "ssi_school_student_graduation."
            "school_student_graduation_batch_user_group"
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

        # 01-create.md -- no batch record is pre-created; the create
        # tour creates one and populates it. Only an eligible student
        # (Enrolled, no Next Grade) needs to exist so Populate finds
        # it.
        cls._create_eligible_student("CR", "Create Eligible")

        # 02-edit.md -- Draft batch to edit. No separate "eligible
        # student" fixture is created here: _get_eligible_student_
        # criteria only restricts by active_enrollment_id.
        # academic_year_id when the batch's own academic_year_id is
        # set, and _create_batch already sets it to the Academic Year
        # of the one line student it creates internally ("TOUR SGB
        # Edit Student", suffix "EB" -- distinct from "01-create"'s
        # "CR" suffix to avoid the "Duplicate code" collision on
        # shared master data codes like school_grade_type). That
        # student is therefore itself the only record guaranteed to
        # match this batch's Populate filter, so the tour re-populate
        # step (school_student_graduation_batch_tour.js test_edit)
        # asserts on "TOUR SGB Edit Student" reappearing after
        # Populate -- a standalone student tied to a different
        # Academic Year would never match this batch's filter and was
        # never actually eligible for it, regardless of naming.
        cls.batch_edit = cls._create_batch("EB", "Edit")

        # 03-delete.md -- Draft batch to delete.
        cls.batch_delete = cls._create_batch("DL", "Delete")

        # 04-confirm.md -- Draft batch (with one line) to confirm.
        cls.batch_confirm = cls._create_batch("CO", "Confirm")

        # 05-approve.md -- Waiting for Approval batch to approve.
        cls.batch_approve = cls._create_batch("AP", "Approve")
        cls.batch_approve.with_user(cls.admin).action_confirm()

        # 06-reject.md -- Waiting for Approval batch to reject.
        cls.batch_reject = cls._create_batch("RJ", "Reject")
        cls.batch_reject.with_user(cls.admin).action_confirm()

        # 10-cancel.md -- Waiting for Approval batch to cancel.
        cls.batch_cancel = cls._create_batch("CN", "Cancel")
        cls.batch_cancel.with_user(cls.admin).action_confirm()

        # 12-restart.md -- Cancelled batch to restart.
        cls.batch_restart = cls._create_batch("RS", "Restart")
        cls.batch_restart.with_user(cls.admin).action_confirm()
        cls.batch_restart.with_user(cls.admin).action_cancel(cls.cancel_reason)

        # 13-reset-number.md -- Draft batch with a manually-set
        # document number.
        cls.batch_reset_number = cls._create_batch("RN", "Reset Number")
        cls.batch_reset_number.write({"name": "TOUR-SGB-MANUAL-001"})

        # 14-restart-approval.md -- Waiting for Approval batch whose
        # approval process is stalled.
        cls.batch_restart_approval = cls._create_batch("RA", "Restart Approval")
        cls.batch_restart_approval.with_user(cls.admin).action_confirm()
        cls.batch_restart_approval.sudo().approval_ids.unlink()
        cls.batch_restart_approval.sudo().write({"approval_template_id": False})

        # 15-print.md -- any state is usable per the IK; a fresh Draft
        # batch is enough.
        cls.batch_print = cls._create_batch("PR", "Print")

        # 16-reload-template-policy.md -- any state is usable per the
        # IK; a fresh Draft batch is enough.
        cls.batch_reload_template_policy = cls._create_batch("RT", "Reload Policy")

    @classmethod
    def _create_eligible_student(cls, suffix, label):
        """Build one Enrolled student eligible for ``action_populate_lines``.

        Creates an isolated grade type / school / grade / grade class
        / academic year & term, then a student brought to the
        Enrolled state with no Next Grade set.

        :param suffix: short unique code suffix for this fixture set.
        :param label: label used to build the student's tour marker
            name "TOUR SGB <label> Student".
        :return: the created ``school_student`` record.
        """
        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR SGB Grade Type %s" % suffix,
                "code": "GTSGB%s" % suffix,
                "sequence": 10,
            }
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR SGB School %s" % suffix,
                "code": "SCHSGB%s" % suffix,
                "grade_type_id": grade_type.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR SGB Grade %s" % suffix,
                "code": "GSGB%s" % suffix,
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR SGB %s Class" % label,
                "code": "CLSGB%s" % suffix,
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR SGB %s Year" % label,
                "code": "AYSGB%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR SGB Term %s" % suffix,
                "code": "TMSGB%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        student_name = "TOUR SGB %s Student" % label
        contact = cls.env["res.partner"].create({"name": "%s Contact" % student_name})
        student = cls.env["school_student"].create(
            {
                "name": student_name,
                "code": "STUSGB%s" % suffix,
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
        return student

    @classmethod
    def _create_batch(cls, suffix, label):
        """Create a Draft batch for state-changing tours.

        The batch's ``academic_year_id`` is set to a uniquely-named
        Academic Year ("TOUR SGB <label> Year") so the tour can find
        the record's row in the list, and one line is added manually
        (not via Populate) so the "at least one student line exists"
        Pre-Condition holds for 04-confirm onward. ``user_id`` is set
        explicitly to ``base.user_admin`` -- see the docstring note in
        ``TestUiSchoolStudentGraduation._create_graduation`` for why
        this is required for the tour's "admin" session to see the
        record at all.

        :param suffix: short unique code suffix for this fixture set.
        :param label: label used to build the batch's tour marker
            year name and the line student's name.
        :return: the created ``school_student_graduation_batch``
            record.
        """
        student = cls._create_eligible_student(suffix, label)
        year = cls.env["school_academic_year"].search(
            [("name", "=", "TOUR SGB %s Year" % label)],
            limit=1,
        )
        return cls.env["school_student_graduation_batch"].create(
            {
                "date": "2025-06-30",
                "academic_year_id": year.id,
                "line_ids": [(0, 0, {"student_id": student.id})],
                "user_id": cls.admin.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_student_graduation_batch``.

        IK: docs/school_student_graduation_batch/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_batch_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_student_graduation_batch``.

        IK: docs/school_student_graduation_batch/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_batch_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_student_graduation_batch``.

        IK: docs/school_student_graduation_batch/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_batch_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_student_graduation_batch``.

        IK: docs/school_student_graduation_batch/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_batch_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_student_graduation_batch``.

        IK: docs/school_student_graduation_batch/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_batch_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_student_graduation_batch``.

        IK: docs/school_student_graduation_batch/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_batch_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_student_graduation_batch``.

        IK: docs/school_student_graduation_batch/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_batch_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``school_student_graduation_batch``.

        IK: docs/school_student_graduation_batch/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_batch_restart",
            login="admin",
        )

    def test_reset_number(self):
        """Run the reset document number tour.

        IK: docs/school_student_graduation_batch/13-reset-number.md
        """
        self.start_tour(
            "/web",
            (
                "ssi_school_student_graduation_school_student_graduation_"
                "batch_reset_number"
            ),
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval process tour.

        IK: docs/school_student_graduation_batch/14-restart-approval.md

        Config Pre-Condition note: same reasoning as
        TestUiSchoolStudentGraduation.test_restart_approval -- this
        HttpCase's setUpClass supplies the missing
        restart_approval_ok policy.template_detail directly.
        """
        self.start_tour(
            "/web",
            (
                "ssi_school_student_graduation_school_student_graduation_"
                "batch_restart_approval"
            ),
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_student_graduation_batch/15-print.md

        Boundary: same reasoning as
        TestUiSchoolStudentGraduation.test_print -- the resulting
        report action is an ``ir.actions.act_url`` download with no
        DOM "finished" signal.
        """
        self.start_tour(
            "/web",
            "ssi_school_student_graduation_school_student_graduation_batch_print",
            login="admin",
        )

    def test_reload_template_policy(self):
        """Run the reload template policy tour.

        IK: docs/school_student_graduation_batch/16-reload-template-policy.md

        Boundary: action_reload_policy_template returns nothing and
        triggers no dialog; the tour only proves the button on the
        Policies tab is reachable and clickable, and that the form
        survives the click without error.
        """
        self.start_tour(
            "/web",
            (
                "ssi_school_student_graduation_school_student_graduation_"
                "batch_reload_template_policy"
            ),
            login="admin",
        )
