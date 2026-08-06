# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolTeacher(HttpSavepointCase):
    """Tour tests for the ``school_teacher`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Prepare the employees, records, and print/sequence data."""
        super().setUpClass()
        # Pre-Condition IK is prepared here -- NOT by clicking through
        # the UI. ``school_teacher_group`` already includes
        # ``base.user_admin`` (security/res_group_data.xml), so no extra
        # group grant is required for the menu to be visible.
        #
        # Pre-Condition for docs/school_teacher/01-create.md: an
        # hr.employee record for the person to be registered as a
        # teacher, picked from the many2one dropdown by the create tour.
        cls.employee_create = cls.env["hr.employee"].create(
            {"name": "TOUR TEACHER EMPLOYEE CREATE"}
        )
        cls.employee_edit = cls.env["hr.employee"].create(
            {"name": "TOUR TEACHER EMPLOYEE EDIT"}
        )
        cls.employee_delete = cls.env["hr.employee"].create(
            {"name": "TOUR TEACHER EMPLOYEE DELETE"}
        )
        cls.employee_deactivate = cls.env["hr.employee"].create(
            {"name": "TOUR TEACHER EMPLOYEE DEACTIVATE"}
        )
        cls.employee_activate = cls.env["hr.employee"].create(
            {"name": "TOUR TEACHER EMPLOYEE ACTIVATE"}
        )
        cls.employee_print = cls.env["hr.employee"].create(
            {"name": "TOUR TEACHER EMPLOYEE PRINT"}
        )

        cls.teacher_edit = cls.env["school_teacher"].create(
            {
                "name": "TOUR TEACHER EDIT",
                "code": "/",
                "employee_id": cls.employee_edit.id,
            }
        )
        cls.teacher_delete = cls.env["school_teacher"].create(
            {
                "name": "TOUR TEACHER DELETE",
                "code": "TOURTCHDEL",
                "employee_id": cls.employee_delete.id,
            }
        )
        cls.teacher_deactivate = cls.env["school_teacher"].create(
            {
                "name": "TOUR TEACHER DEACTIVATE",
                "code": "TOURTCHDEA",
                "employee_id": cls.employee_deactivate.id,
            }
        )
        cls.teacher_activate = cls.env["school_teacher"].create(
            {
                "name": "TOUR TEACHER ACTIVATE",
                "code": "TOURTCHACT",
                "employee_id": cls.employee_activate.id,
                "active": False,
            }
        )

        # Pre-Condition for Generate Code
        # (docs/school_teacher/01-create.md and 02-edit.md): an active
        # ``sequence.template`` for this model is required, or clicking
        # the button raises a UserError instead of assigning a code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Teacher Code Sequence",
                "code": "ssi_school.tour.school_teacher",
                "prefix": "TOURSEQTCH",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Teacher Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("school_teacher"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("school_teacher", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("school_teacher", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        # Pre-Condition for the print tour
        # (docs/school_teacher/06-print.md): a ``print_document_type``
        # linking a report to ``school_teacher`` is required for the
        # wizard to have a report to offer -- without it the wizard
        # still opens but the report list is empty. The tour itself
        # never selects nor prints the report (see test_print
        # docstring), so the report action is a placeholder that is
        # never rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Teacher Report",
                "model": "school_teacher",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school.tour_school_teacher_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Teacher Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_teacher"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.teacher_print = cls.env["school_teacher"].create(
            {
                "name": "TOUR TEACHER PRINT",
                "code": "TOURTCHPRN",
                "employee_id": cls.employee_print.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_teacher``.

        IK: docs/school_teacher/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_teacher_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_teacher``.

        IK: docs/school_teacher/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_teacher_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_teacher``.

        IK: docs/school_teacher/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_teacher_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``school_teacher``.

        IK: docs/school_teacher/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_teacher_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``school_teacher``.

        IK: docs/school_teacher/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_teacher_activate",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_teacher/06-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour(
            "/web",
            "ssi_school_school_teacher_print",
            login="admin",
        )
