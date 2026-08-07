# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiCrmLead(HttpSavepointCase):
    """UI/UX tour tests for the ``crm.lead`` IK this module adds.

    Covers the additional fields inserted onto the standard CRM Lead
    form and the "Create Admission Form"/"Admission Test" conversion
    buttons. Every ``test_*`` method runs the tour pairing with the IK
    file named in its docstring (``docs/crm_lead/NN-*.md``).
    Pre-Condition data is prepared here in Python, never through UI
    steps.
    """

    @classmethod
    def setUpClass(cls):
        """Build the academic/school structure and the tour fixtures."""
        super().setUpClass()

        # SavepointCase.setUpClass runs cls.env as SUPERUSER_ID (odoo/
        # tests/common.py), so any record created via cls.env.create()
        # without an explicit user_id defaults "Responsible" (user_id,
        # mixin.transaction._default_user_id -> self.env.user.id) to the
        # superuser, NOT "admin". The internal-user record rules on
        # school_admission_form/school_admission_test
        # ([('user_id','=',user.id)], base.group_user) then hide every
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
        cls.env.ref("crm.group_use_lead").write(
            {"users": [(4, cls.admin_user.id)]}
        )

        # -- Academic / school structure (Pre-Condition Data), shared by
        # every tour in this class ------------------------------------
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR LEAD ADF Academic Year",
                "code": "TOURLEADADFAY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR LEAD ADF Term",
                "code": "TOURLEADADFT",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.academic_year.id,
                "is_open_admission": True,
            }
        )
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR LEAD ADF Grade Type", "code": "TOURLEADADFGT"}
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR LEAD ADF School",
                "code": "TOURLEADADFSCH",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "TOUR-LEAD-ADF-GRADE",
                "code": "TOURLEADADFG",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )

        # 02-create-admission-form.md -- lead with School/Student already
        # set so the wizard's context defaults pre-fill them; Pricelist,
        # Grade, and Parent are left for the tour to pick (the IK states
        # Grade is deliberately NOT pre-filled from the lead's own Grade
        # field).
        cls.student_adf = cls.env["res.partner"].create(
            {"name": "TOUR-LEAD-ADF-STUDENT", "is_company": False}
        )
        cls.lead_admission_form = (
            cls.env["crm.lead"]
            .with_user(cls.admin_user)
            .create(
                {
                    "name": "TOUR-LEAD-ADF-001",
                    "type": "lead",
                    "user_id": cls.admin_user.id,
                    "school_id": cls.school.id,
                    "student_id": cls.student_adf.id,
                }
            )
        )

        # 03-open-admission-test.md -- a Draft school_admission_form and
        # school_admission_test linked to it, created directly via ORM
        # (out of scope for this tour: the create-admission-form wizard
        # itself is exercised by 02-create-admission-form.md), then a
        # lead whose admission_form_id is set. crm.lead.admission_test_id
        # is `related="admission_form_id.admission_test_id", store=True`,
        # so it is populated automatically once the lead is created with
        # admission_form_id already pointing at a form that already has
        # its admission_test_ids populated -- hence the creation order
        # below: form, then test (linking back to the form), then lead.
        cls.student_oat = cls.env["res.partner"].create(
            {"name": "TOUR-LEAD-OAT-STUDENT", "is_company": False}
        )
        cls.parent_oat = cls.env["res.partner"].create(
            {"name": "TOUR-LEAD-OAT-PARENT"}
        )
        cls.pricelist_oat = cls.env["product.pricelist"].create(
            {
                "name": "TOUR-LEAD-OAT-PRICELIST",
                "currency_id": cls.env.company.currency_id.id,
            }
        )
        # journal_id/account_id are required=True on school_admission_form
        # (inherited from mixin.account_move -- ssi_accounting_entry_mixin).
        # The UI fills them via _onchange_fee_template_id when Fee
        # Template is selected on the form, but that onchange never fires
        # on a plain Python .create() call, so both are set explicitly.
        income_type = cls.env.ref("account.data_account_type_revenue")
        cls.income_account = cls.env["account.account"].create(
            {
                "name": "TOUR LEAD OAT Income",
                "code": "TOURLEADOATINC",
                "user_type_id": income_type.id,
            }
        )
        cls.journal = cls.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        cls.admission_form_oat = cls.env["school_admission_form"].create(
            {
                "academic_year_id": cls.academic_year.id,
                "academic_term_id": cls.academic_term.id,
                "student_id": cls.student_oat.id,
                "parent_id": cls.parent_oat.id,
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "pricelist_id": cls.pricelist_oat.id,
                "currency_id": cls.pricelist_oat.currency_id.id,
                "journal_id": cls.journal.id,
                "account_id": cls.income_account.id,
                "user_id": cls.admin_user.id,
            }
        )
        cls.admission_test_oat = cls.env["school_admission_test"].create(
            {
                "academic_year_id": cls.academic_year.id,
                "academic_term_id": cls.academic_term.id,
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "admission_form_id": cls.admission_form_oat.id,
                "student_id": cls.student_oat.id,
                "user_id": cls.admin_user.id,
            }
        )
        cls.lead_admission_test = (
            cls.env["crm.lead"]
            .with_user(cls.admin_user)
            .create(
                {
                    "name": "TOUR-LEAD-OAT-001",
                    "type": "lead",
                    "user_id": cls.admin_user.id,
                    "admission_form_id": cls.admission_form_oat.id,
                }
            )
        )

    def test_create(self):
        """Run the delta-only create tour for ``crm.lead``.

        IK: docs/crm_lead/01-create.md
        """
        self.start_tour(
            "/web", "ssi_school_admission_lead_crm_lead_create", login="admin"
        )

    def test_create_admission_form(self):
        """Run the Create Admission Form conversion tour for ``crm.lead``.

        IK: docs/crm_lead/02-create-admission-form.md
        """
        self.start_tour(
            "/web",
            "ssi_school_admission_lead_crm_lead_create_admission_form",
            login="admin",
        )

    def test_open_admission_test(self):
        """Run the Open Admission Test tour for ``crm.lead``.

        IK: docs/crm_lead/03-open-admission-test.md
        """
        self.start_tour(
            "/web",
            "ssi_school_admission_lead_crm_lead_open_admission_test",
            login="admin",
        )
