# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiCrmLead(HttpSavepointCase):
    """UI/UX tour tests for the ``crm.lead`` IK this module adds.

    Covers the additional fields inserted onto the standard CRM Lead
    form and the "Create Admission" conversion button. Every
    ``test_*`` method runs the tour pairing with the IK file named in
    its docstring (``docs/crm_lead/NN-*.md``). Pre-Condition data is
    prepared here in Python, never through UI steps.
    """

    @classmethod
    def setUpClass(cls):
        """Build the academic/school structure and the tour fixtures."""
        super().setUpClass()

        # SavepointCase.setUpClass runs cls.env as SUPERUSER_ID (odoo/
        # tests/common.py), so any record created via cls.env.create()
        # without an explicit user_id defaults "Responsible" (user_id,
        # mixin.transaction._default_user_id -> self.env.user.id) to the
        # superuser, NOT "admin". school_admission_internal_user_rule
        # ([('user_id','=',user.id)], base.group_user) then hides every
        # such fixture from the "admin" tour session -- 0 rows in every
        # list, no crash. Every fixture below sets user_id explicitly.
        cls.admin_user = cls.env.ref("base.user_admin")

        # Pre-Condition (Config): the CRM app's Leads feature is enabled
        # -- crm_menu_leads is gated by groups="crm.group_use_lead", and
        # its parent crm_menu_root by groups=
        # "sales_team.group_sale_salesman,sales_team.group_sale_manager".
        # Without these the tour dies on its FIRST step: neither the CRM
        # app icon nor the Leads menu is ever rendered for "admin"
        # (structure-and-runner.md §4, "Menu ter-gate grup").
        cls.env.ref("sales_team.group_sale_manager").write(
            {"users": [(4, cls.admin_user.id)]}
        )
        cls.env.ref("crm.group_use_lead").write({"users": [(4, cls.admin_user.id)]})

        # -- Academic / school structure (Pre-Condition Data) -----------
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR LEAD ADM Academic Year",
                "code": "TOURLEADADMAY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR LEAD ADM Term",
                "code": "TOURLEADADMT",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.academic_year.id,
                "is_open_admission": True,
            }
        )
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR LEAD ADM Grade Type", "code": "TOURLEADADMGT"}
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR LEAD ADM School",
                "code": "TOURLEADADMSCH",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "TOUR-LEAD-ADM-GRADE",
                "code": "TOURLEADADMG",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )

        # 02-create-admission.md -- lead with School/Student already set
        # so the wizard's context defaults pre-fill them; only Grade is
        # left for the tour to pick.
        cls.student = cls.env["res.partner"].create(
            {"name": "TOUR-LEAD-ADM-STUDENT", "is_company": False}
        )
        cls.lead_create_admission = (
            cls.env["crm.lead"]
            .with_user(cls.admin_user)
            .create(
                {
                    "name": "TOUR-LEAD-ADM-001",
                    "type": "lead",
                    "user_id": cls.admin_user.id,
                    "school_id": cls.school.id,
                    "student_id": cls.student.id,
                }
            )
        )

    def test_create(self):
        """Run the delta-only create tour for ``crm.lead``.

        IK: docs/crm_lead/01-create.md
        """
        self.start_tour("/web", "ssi_school_lead_crm_lead_create", login="admin")

    def test_create_admission(self):
        """Run the Create Admission conversion tour for ``crm.lead``.

        IK: docs/crm_lead/02-create-admission.md
        """
        self.start_tour(
            "/web", "ssi_school_lead_crm_lead_create_admission", login="admin"
        )
