# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolAcademicYear(HttpSavepointCase):
    """Tour tests for the ``school_academic_year`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Prepare the records and print/sequence data the tours need."""
        super().setUpClass()
        # Pre-Condition IK is prepared here -- NOT by clicking through
        # the UI. ``school_academic_year_group`` already includes
        # ``base.user_admin`` (security/res_group_data.xml), so no extra
        # group grant is required for the menu to be visible.
        cls.academic_year_edit = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ACADEMIC YEAR EDIT",
                "code": "/",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.academic_year_delete = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ACADEMIC YEAR DELETE",
                "code": "TOURAYDEL",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.academic_year_deactivate = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ACADEMIC YEAR DEACTIVATE",
                "code": "TOURAYDEA",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.academic_year_activate = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ACADEMIC YEAR ACTIVATE",
                "code": "TOURAYACT",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
                "active": False,
            }
        )

        # Pre-Condition for Generate Code
        # (docs/school_academic_year/01-create.md and 02-edit.md): an
        # active ``sequence.template`` for this model is required, or
        # clicking the button raises a UserError instead of assigning a
        # code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Academic Year Code Sequence",
                "code": "ssi_school.tour.school_academic_year",
                "prefix": "TOURSEQAY",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Academic Year Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("school_academic_year"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("school_academic_year", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("school_academic_year", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        # Pre-Condition for the print tour
        # (docs/school_academic_year/06-print.md): a
        # ``print_document_type`` linking a report to
        # ``school_academic_year`` is required for the wizard to have a
        # report to offer -- without it the wizard still opens but the
        # report list is empty. The tour itself never selects nor prints
        # the report (see test_print docstring), so the report action is
        # a placeholder that is never rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Academic Year Report",
                "model": "school_academic_year",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school.tour_school_academic_year_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Academic Year Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_academic_year"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.academic_year_print = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ACADEMIC YEAR PRINT",
                "code": "TOURAYPRN",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )

    def test_create(self):
        """Run the create tour for ``school_academic_year``.

        IK: docs/school_academic_year/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_academic_year_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_academic_year``.

        IK: docs/school_academic_year/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_academic_year_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_academic_year``.

        IK: docs/school_academic_year/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_academic_year_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``school_academic_year``.

        IK: docs/school_academic_year/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_academic_year_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``school_academic_year``.

        IK: docs/school_academic_year/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_academic_year_activate",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_academic_year/06-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour(
            "/web",
            "ssi_school_school_academic_year_print",
            login="admin",
        )
