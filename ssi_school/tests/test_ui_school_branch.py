# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolBranch(HttpSavepointCase):
    """Tour tests for the ``school_branch`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records and configuration required by the tours."""
        super().setUpClass()
        cls.branch_edit = cls.env["school_branch"].create(
            {
                "name": "TOUR Branch Edit",
                "code": "/",
            }
        )
        cls.branch_delete = cls.env["school_branch"].create(
            {
                "name": "TOUR Branch Delete",
                "code": "/",
            }
        )
        cls.branch_deactivate = cls.env["school_branch"].create(
            {
                "name": "TOUR Branch Deactivate",
                "code": "/",
            }
        )
        cls.branch_activate = cls.env["school_branch"].create(
            {
                "name": "TOUR Branch Activate",
                "code": "/",
                "active": False,
            }
        )

        # Pre-Condition for Generate Code (docs/school_branch/01-create.md
        # and docs/school_branch/02-edit.md): an active sequence.template
        # for this model is required, or clicking the button raises a
        # UserError instead of assigning a code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Branch Code Sequence",
                "code": "ssi_school.tour.school_branch",
                "prefix": "TOURSEQBRC",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Branch Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("school_branch"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("school_branch", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("school_branch", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        # Pre-Condition for the print tour (docs/school_branch/06-print.md):
        # a print_document_type linking a report to `school_branch` is
        # required for the wizard to have a report to offer -- without it
        # the wizard still opens but the report list is empty. The tour
        # itself never selects nor prints the report (see test_print
        # docstring), so the report action is a placeholder that is never
        # rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Branch Report",
                "model": "school_branch",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school.tour_school_branch_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Branch Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_branch"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.branch_print = cls.env["school_branch"].create(
            {
                "name": "TOUR PRINT BRANCH",
                "code": "TOURPRNBRC",
            }
        )

    def test_create(self):
        """Run the create tour for ``school_branch``.

        IK: docs/school_branch/01-create.md
        """
        self.start_tour("/web", "ssi_school_school_branch_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``school_branch``.

        IK: docs/school_branch/02-edit.md
        """
        self.start_tour("/web", "ssi_school_school_branch_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``school_branch``.

        IK: docs/school_branch/03-delete.md
        """
        self.start_tour("/web", "ssi_school_school_branch_delete", login="admin")

    def test_deactivate(self):
        """Run the deactivate tour for ``school_branch``.

        IK: docs/school_branch/04-deactivate.md
        """
        self.start_tour("/web", "ssi_school_school_branch_deactivate", login="admin")

    def test_activate(self):
        """Run the activate tour for ``school_branch``.

        IK: docs/school_branch/05-activate.md
        """
        self.start_tour("/web", "ssi_school_school_branch_activate", login="admin")

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_branch/06-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour("/web", "ssi_school_school_branch_print", login="admin")
