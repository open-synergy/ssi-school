# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolStudent(HttpSavepointCase):
    """Tour tests for the ``school_student`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Prepare the school, contacts, records, and print data."""
        super().setUpClass()
        # Pre-Condition IK is prepared here -- NOT by clicking through
        # the UI. ``school_student_group`` already includes
        # ``base.user_admin`` (security/res_group_data.xml), so no extra
        # group grant is required for the menu to be visible.
        #
        # Pre-Condition for docs/school_student/01-create.md: at least
        # one School must already exist, picked from the many2one
        # dropdown by the create tour.
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR Student Grade Type",
                "code": "TOURSTUGT",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR STUDENT SCHOOL",
                "code": "TOURSTUSCH",
                "grade_type_id": cls.grade_type.id,
            }
        )

        # Pre-Condition for docs/school_student/01-create.md: a
        # res.partner contact for the student, picked from the
        # many2one dropdown by the create tour.
        cls.contact_create = cls.env["res.partner"].create(
            {"name": "TOUR STUDENT CONTACT CREATE"}
        )
        cls.contact_edit = cls.env["res.partner"].create(
            {"name": "TOUR STUDENT CONTACT EDIT"}
        )
        cls.contact_delete = cls.env["res.partner"].create(
            {"name": "TOUR STUDENT CONTACT DELETE"}
        )
        cls.contact_deactivate = cls.env["res.partner"].create(
            {"name": "TOUR STUDENT CONTACT DEACTIVATE"}
        )
        cls.contact_activate = cls.env["res.partner"].create(
            {"name": "TOUR STUDENT CONTACT ACTIVATE"}
        )
        cls.contact_print = cls.env["res.partner"].create(
            {"name": "TOUR STUDENT CONTACT PRINT"}
        )

        cls.student_edit = cls.env["school_student"].create(
            {
                "name": "TOUR STUDENT EDIT",
                "code": "/",
                "contact_id": cls.contact_edit.id,
                "school_id": cls.school.id,
            }
        )
        cls.student_delete = cls.env["school_student"].create(
            {
                "name": "TOUR STUDENT DELETE",
                "code": "TOURSTUDEL",
                "contact_id": cls.contact_delete.id,
                "school_id": cls.school.id,
            }
        )
        cls.student_deactivate = cls.env["school_student"].create(
            {
                "name": "TOUR STUDENT DEACTIVATE",
                "code": "TOURSTUDEA",
                "contact_id": cls.contact_deactivate.id,
                "school_id": cls.school.id,
            }
        )
        cls.student_activate = cls.env["school_student"].create(
            {
                "name": "TOUR STUDENT ACTIVATE",
                "code": "TOURSTUACT",
                "contact_id": cls.contact_activate.id,
                "school_id": cls.school.id,
                "active": False,
            }
        )

        # Pre-Condition for Generate Code
        # (docs/school_student/01-create.md and 02-edit.md): an active
        # ``sequence.template`` for this model is required, or clicking
        # the button raises a UserError instead of assigning a code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Student Code Sequence",
                "code": "ssi_school.tour.school_student",
                "prefix": "TOURSEQSTU",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Student Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("school_student"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("school_student", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("school_student", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        # Pre-Condition for the print tour
        # (docs/school_student/06-print.md): a ``print_document_type``
        # linking a report to ``school_student`` is required for the
        # wizard to have a report to offer -- without it the wizard
        # still opens but the report list is empty. The tour itself
        # never selects nor prints the report (see test_print
        # docstring), so the report action is a placeholder that is
        # never rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Student Report",
                "model": "school_student",
                "report_type": "qweb-pdf",
                "report_name": "ssi_school.tour_school_student_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Student Print Type",
                "model_id": cls.env["ir.model"]._get_id("school_student"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.student_print = cls.env["school_student"].create(
            {
                "name": "TOUR STUDENT PRINT",
                "code": "TOURSTUPRN",
                "contact_id": cls.contact_print.id,
                "school_id": cls.school.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_student``.

        IK: docs/school_student/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_student``.

        IK: docs/school_student/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_student``.

        IK: docs/school_student/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``school_student``.

        IK: docs/school_student/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``school_student``.

        IK: docs/school_student/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_activate",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/school_student/06-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal -- clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour(
            "/web",
            "ssi_school_school_student_print",
            login="admin",
        )
