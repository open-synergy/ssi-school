# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolGradeType(HttpSavepointCase):
    """Tour tests for the ``school_grade_type`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records and configuration required by the tours."""
        super().setUpClass()
        cls.grade_type_edit = cls.env["school_grade_type"].create(
            {
                "name": "TOUR Grade Type Edit",
                "code": "/",
            }
        )
        cls.grade_type_delete = cls.env["school_grade_type"].create(
            {
                "name": "TOUR Grade Type Delete",
                "code": "/",
            }
        )
        cls.grade_type_deactivate = cls.env["school_grade_type"].create(
            {
                "name": "TOUR Grade Type Deactivate",
                "code": "/",
            }
        )
        cls.grade_type_activate = cls.env["school_grade_type"].create(
            {
                "name": "TOUR Grade Type Activate",
                "code": "/",
                "active": False,
            }
        )

        # Pre-Condition for Generate Code (docs/school_grade_type/
        # 01-create.md and docs/school_grade_type/02-edit.md): an active
        # sequence.template for this model is required, or clicking the
        # button raises a UserError instead of assigning a code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Grade Type Code Sequence",
                "code": "ssi_school.tour.school_grade_type",
                "prefix": "TOURSEQGRT",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Grade Type Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("school_grade_type"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("school_grade_type", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("school_grade_type", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        # Pre-Condition for the print tour (docs/school_grade_type/
        # 06-print.md): a print_document_type linking a report to
        # `school_grade_type` is required for the wizard to have a report
        # to offer -- without it the wizard still opens but the report
        # list is empty. The tour itself never selects nor prints the
        # report (see test_print docstring), so the report action is a
        # placeholder that is never rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Grade Type Report",
                "model": "school_grade_type",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school.tour_school_grade_type_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Grade Type Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_grade_type"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.grade_type_print = cls.env["school_grade_type"].create(
            {
                "name": "TOUR PRINT GRADE TYPE",
                "code": "TOURPRNGRT",
            }
        )

    def test_create(self):
        """Run the create tour for ``school_grade_type``.

        IK: docs/school_grade_type/01-create.md
        """
        self.start_tour("/web", "ssi_school_school_grade_type_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``school_grade_type``.

        IK: docs/school_grade_type/02-edit.md
        """
        self.start_tour("/web", "ssi_school_school_grade_type_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``school_grade_type``.

        IK: docs/school_grade_type/03-delete.md
        """
        self.start_tour("/web", "ssi_school_school_grade_type_delete", login="admin")

    def test_deactivate(self):
        """Run the deactivate tour for ``school_grade_type``.

        IK: docs/school_grade_type/04-deactivate.md
        """
        self.start_tour(
            "/web", "ssi_school_school_grade_type_deactivate", login="admin"
        )

    def test_activate(self):
        """Run the activate tour for ``school_grade_type``.

        IK: docs/school_grade_type/05-activate.md
        """
        self.start_tour("/web", "ssi_school_school_grade_type_activate", login="admin")

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_grade_type/06-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour("/web", "ssi_school_school_grade_type_print", login="admin")
