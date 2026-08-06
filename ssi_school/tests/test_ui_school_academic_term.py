# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolAcademicTerm(HttpSavepointCase):
    """UI/UX tour tests for ``school_academic_term``.

    Every ``test_*`` method below runs the tour pairing with the IK file
    named in its docstring (``docs/school_academic_term/NN-*.md``).
    Pre-Condition data required by each IK is prepared here in Python --
    never through UI steps -- following the tour authoring doctrine:
    prerequisite/background data belongs to ``setUpClass``, the tour
    itself only exercises the click-flow documented in the IK. The
    ``school_academic_term_group`` menu/model access group already
    includes ``base.user_admin`` by default
    (``security/res_group_data.xml``), so no extra group grant is needed
    here.
    """

    @classmethod
    def setUpClass(cls):
        """Create the academic year and term fixtures the tours exercise.

        A single, wide-ranged ``school_academic_year`` ("TOUR SAT Academic
        Year", 2026-01-01 to 2026-12-31) is shared by every term fixture
        below so all of their dates comfortably satisfy
        ``_check_date_coherence`` without needing a dedicated year per
        fixture. Each term's ``code`` is left as ``"/"`` (excluded from
        the unique-code check by
        ``mixin.master_data._check_duplicate_code``) so several fixtures
        can share it, and so the Generate Code inline action has
        something to do in the create/edit tours.
        """
        super().setUpClass()

        cls.year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR SAT Academic Year",
                "code": "/",
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
            }
        )

        # Pre-Condition for docs/school_academic_term/02-edit.md.
        cls.term_edit = cls._create_term("TOUR SAT Edit")
        # Pre-Condition for docs/school_academic_term/03-delete.md.
        cls.term_delete = cls._create_term("TOUR SAT Delete")
        # Pre-Condition for docs/school_academic_term/04-deactivate.md.
        cls.term_deactivate = cls._create_term("TOUR SAT Deactivate")
        # Pre-Condition for docs/school_academic_term/05-activate.md: the
        # record is currently archived.
        cls.term_activate = cls._create_term("TOUR SAT Activate", active=False)

        # Pre-Condition for docs/school_academic_term/06-start.md: status
        # is Unstarted (the model's own "draft" default -- no extra call
        # needed).
        cls.term_start = cls._create_term("TOUR SAT Start")

        # Pre-Condition for docs/school_academic_term/07-finish.md: status
        # is On progress. Reached by calling action_open() directly in
        # Python, NOT by clicking through the UI -- the create/start click
        # flow is exercised by its own tour, not repeated here.
        cls.term_finish = cls._create_term("TOUR SAT Finish")
        cls.term_finish.action_open()

        # Pre-Condition for docs/school_academic_term/08-restart.md:
        # status is On progress (one of the two valid Restart source
        # states).
        cls.term_restart = cls._create_term("TOUR SAT Restart")
        cls.term_restart.action_open()

        # Pre-Condition for docs/school_academic_term/09-open-enrollment.md:
        # Enrollment State is Close (the model's own default -- no extra
        # call needed).
        cls.term_open_enrollment = cls._create_term("TOUR SAT Open Enrollment")

        # Pre-Condition for docs/school_academic_term/10-close-enrollment.md:
        # Enrollment State is Open for Enrollment.
        cls.term_close_enrollment = cls._create_term("TOUR SAT Close Enrollment")
        cls.term_close_enrollment.action_open_enrollment()

        # Pre-Condition for docs/school_academic_term/01-create.md and
        # 02-edit.md: an active sequence.template for this model is
        # required, or clicking Generate Code raises a UserError instead
        # of assigning a code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Academic Term Code Sequence",
                "code": "ssi_school.tour.school_academic_term",
                "prefix": "TOURSEQSAT",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Academic Term Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("school_academic_term"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("school_academic_term", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("school_academic_term", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        # Pre-Condition for docs/school_academic_term/11-print.md: a
        # print_document_type linking a report to school_academic_term is
        # required for the wizard to have a report to offer -- without it
        # the wizard still opens but the report list is empty. The tour
        # itself never selects nor prints the report (see test_print
        # docstring), so the report action is a placeholder that is never
        # rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Academic Term Report",
                "model": "school_academic_term",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school.tour_school_academic_term_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Academic Term Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_academic_term"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.term_print = cls._create_term("TOUR SAT Print")

    @classmethod
    def _create_term(cls, name, active=True):
        """Pre-Condition helper: create a draft ``school_academic_term``.

        :param name: unique record name the tour locates via ``:contains``.
        :param active: initial value of the ``active`` field.
        :return: the created ``school_academic_term`` record.
        """
        return cls.env["school_academic_term"].create(
            {
                "name": name,
                "code": "/",
                "year_id": cls.year.id,
                "date_start": "2026-01-15",
                "date_end": "2026-06-15",
                "active": active,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_academic_term``.

        IK: docs/school_academic_term/01-create.md
        """
        self.start_tour("/web", "ssi_school_school_academic_term_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``school_academic_term``.

        IK: docs/school_academic_term/02-edit.md
        """
        self.start_tour("/web", "ssi_school_school_academic_term_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``school_academic_term``.

        IK: docs/school_academic_term/03-delete.md
        """
        self.start_tour("/web", "ssi_school_school_academic_term_delete", login="admin")

    def test_deactivate(self):
        """Run the deactivate tour for ``school_academic_term``.

        IK: docs/school_academic_term/04-deactivate.md
        """
        self.start_tour(
            "/web", "ssi_school_school_academic_term_deactivate", login="admin"
        )

    def test_activate(self):
        """Run the activate tour for ``school_academic_term``.

        IK: docs/school_academic_term/05-activate.md
        """
        self.start_tour(
            "/web", "ssi_school_school_academic_term_activate", login="admin"
        )

    def test_start(self):
        """Run the start tour for ``school_academic_term``.

        IK: docs/school_academic_term/06-start.md
        """
        self.start_tour("/web", "ssi_school_school_academic_term_start", login="admin")

    def test_finish(self):
        """Run the finish tour for ``school_academic_term``.

        IK: docs/school_academic_term/07-finish.md
        """
        self.start_tour("/web", "ssi_school_school_academic_term_finish", login="admin")

    def test_restart(self):
        """Run the restart tour for ``school_academic_term``.

        IK: docs/school_academic_term/08-restart.md
        """
        self.start_tour(
            "/web", "ssi_school_school_academic_term_restart", login="admin"
        )

    def test_open_enrollment(self):
        """Run the open enrollment tour for ``school_academic_term``.

        IK: docs/school_academic_term/09-open-enrollment.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_academic_term_open_enrollment",
            login="admin",
        )

    def test_close_enrollment(self):
        """Run the close enrollment tour for ``school_academic_term``.

        IK: docs/school_academic_term/10-close-enrollment.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_academic_term_close_enrollment",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_academic_term/11-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour("/web", "ssi_school_school_academic_term_print", login="admin")
