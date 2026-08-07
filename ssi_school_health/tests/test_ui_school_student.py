# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolStudent(HttpSavepointCase):
    """Tour tests for the ``school_student`` Health tab delta."""

    @classmethod
    def setUpClass(cls):
        """Prepare the school, contact, and record used by the tours.

        Pre-Condition IK is prepared here -- NOT by clicking through the
        UI. ``school_student_group`` already includes ``base.user_admin``
        (``ssi_school``, ``security/res_group_data.xml``), so no extra
        group grant is required for the menu or the Health tab to be
        visible -- the tab is not gated by any group.
        """
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR Health Grade Type",
                "code": "TOURHLTHGT",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR HEALTH SCHOOL",
                "code": "TOURHLTHSCH",
                "grade_type_id": cls.grade_type.id,
            }
        )

        # Pre-Condition for docs/school_student/02-edit.md: an existing
        # Student record must already exist, found and opened by the edit
        # tour. Not needed for the create tour, which only exercises a
        # brand-new (unsaved) record.
        cls.contact_edit = cls.env["res.partner"].create(
            {"name": "TOUR STUDENT HEALTH CONTACT EDIT"}
        )
        cls.student_edit = cls.env["school_student"].create(
            {
                "name": "TOUR STUDENT HEALTH EDIT",
                "code": "/",
                "contact_id": cls.contact_edit.id,
                "school_id": cls.school.id,
            }
        )

    def test_create(self):
        """Run the Health tab delta tour for the create form.

        IK: docs/school_student/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_health_school_student_create",
            login="admin",
        )

    def test_edit(self):
        """Run the Health tab delta tour for the edit form.

        IK: docs/school_student/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_health_school_student_edit",
            login="admin",
        )
