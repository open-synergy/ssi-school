# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolGrade(HttpSavepointCase):
    """Tour tests for the ``school_grade`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records and configuration required by the tours."""
        super().setUpClass()
        # Pre-Condition IK: at least one Grade Type already exists.
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR Grade School Grade Type",
                "code": "/",
            }
        )
        cls.grade_edit = cls.env["school_grade"].create(
            {
                "name": "TOUR Grade Edit",
                "code": "/",
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_delete = cls.env["school_grade"].create(
            {
                "name": "TOUR Grade Delete",
                "code": "/",
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_deactivate = cls.env["school_grade"].create(
            {
                "name": "TOUR Grade Deactivate",
                "code": "/",
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_activate = cls.env["school_grade"].create(
            {
                "name": "TOUR Grade Activate",
                "code": "/",
                "type_id": cls.grade_type.id,
                "active": False,
            }
        )

        # Pre-Condition for Generate Code (docs/school_grade/01-create.md
        # and docs/school_grade/02-edit.md): an active sequence.template
        # for this model is required, or clicking the button raises a
        # UserError instead of assigning a code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Grade Code Sequence",
                "code": "ssi_school.tour.school_grade",
                "prefix": "TOURSEQGRD",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Grade Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("school_grade"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("school_grade", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("school_grade", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        # Pre-Condition for the print tour (docs/school_grade/06-print.md):
        # a print_document_type linking a report to `school_grade` is
        # required for the wizard to have a report to offer -- without it
        # the wizard still opens but the report list is empty. The tour
        # itself never selects nor prints the report (see test_print
        # docstring), so the report action is a placeholder that is never
        # rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Grade Report",
                "model": "school_grade",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school.tour_school_grade_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Grade Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_grade"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.grade_print = cls.env["school_grade"].create(
            {
                "name": "TOUR PRINT GRADE",
                "code": "TOURPRNGRD",
                "type_id": cls.grade_type.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_grade``.

        IK: docs/school_grade/01-create.md
        """
        self.start_tour("/web", "ssi_school_school_grade_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``school_grade``.

        IK: docs/school_grade/02-edit.md
        """
        self.start_tour("/web", "ssi_school_school_grade_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``school_grade``.

        IK: docs/school_grade/03-delete.md
        """
        self.start_tour("/web", "ssi_school_school_grade_delete", login="admin")

    def test_deactivate(self):
        """Run the deactivate tour for ``school_grade``.

        IK: docs/school_grade/04-deactivate.md
        """
        self.start_tour("/web", "ssi_school_school_grade_deactivate", login="admin")

    def test_activate(self):
        """Run the activate tour for ``school_grade``.

        IK: docs/school_grade/05-activate.md
        """
        self.start_tour("/web", "ssi_school_school_grade_activate", login="admin")

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_grade/06-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour("/web", "ssi_school_school_grade_print", login="admin")
