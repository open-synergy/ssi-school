# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolGradeClass(HttpSavepointCase):
    """Tour tests for the ``school_grade_class`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records and configuration required by the tours."""
        super().setUpClass()
        # Pre-Condition IK: at least one School and a matching Grade already
        # exist.
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR Grade Class School Grade Type",
                "code": "/",
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR Grade Class School",
                "code": "/",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "TOUR Grade Class Grade",
                "code": "/",
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_class_edit = cls.env["school_grade_class"].create(
            {
                "name": "TOUR Grade Class Edit",
                "code": "/",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
            }
        )
        cls.grade_class_delete = cls.env["school_grade_class"].create(
            {
                "name": "TOUR Grade Class Delete",
                "code": "/",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
            }
        )
        cls.grade_class_deactivate = cls.env["school_grade_class"].create(
            {
                "name": "TOUR Grade Class Deactivate",
                "code": "/",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
            }
        )
        cls.grade_class_activate = cls.env["school_grade_class"].create(
            {
                "name": "TOUR Grade Class Activate",
                "code": "/",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "active": False,
            }
        )

        # Pre-Condition for Generate Code (docs/school_grade_class/
        # 01-create.md and docs/school_grade_class/02-edit.md): an active
        # sequence.template for this model is required, or clicking the
        # button raises a UserError instead of assigning a code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Grade Class Code Sequence",
                "code": "ssi_school.tour.school_grade_class",
                "prefix": "TOURSEQGRC",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Grade Class Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("school_grade_class"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("school_grade_class", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("school_grade_class", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        # Pre-Condition for the print tour (docs/school_grade_class/
        # 06-print.md): a print_document_type linking a report to
        # `school_grade_class` is required for the wizard to have a report
        # to offer -- without it the wizard still opens but the report
        # list is empty. The tour itself never selects nor prints the
        # report (see test_print docstring), so the report action is a
        # placeholder that is never rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Grade Class Report",
                "model": "school_grade_class",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school.tour_school_grade_class_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Grade Class Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_grade_class"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.grade_class_print = cls.env["school_grade_class"].create(
            {
                "name": "TOUR PRINT GRADE CLASS",
                "code": "TOURPRNGRC",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_grade_class``.

        IK: docs/school_grade_class/01-create.md
        """
        self.start_tour("/web", "ssi_school_school_grade_class_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``school_grade_class``.

        IK: docs/school_grade_class/02-edit.md
        """
        self.start_tour("/web", "ssi_school_school_grade_class_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``school_grade_class``.

        IK: docs/school_grade_class/03-delete.md
        """
        self.start_tour("/web", "ssi_school_school_grade_class_delete", login="admin")

    def test_deactivate(self):
        """Run the deactivate tour for ``school_grade_class``.

        IK: docs/school_grade_class/04-deactivate.md
        """
        self.start_tour(
            "/web", "ssi_school_school_grade_class_deactivate", login="admin"
        )

    def test_activate(self):
        """Run the activate tour for ``school_grade_class``.

        IK: docs/school_grade_class/05-activate.md
        """
        self.start_tour("/web", "ssi_school_school_grade_class_activate", login="admin")

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_grade_class/06-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour("/web", "ssi_school_school_grade_class_print", login="admin")
