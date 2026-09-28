# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolAdmissionFeeAnalysis(HttpSavepointCase):
    """UI/UX tour test for the ``school_admission_fee_analysis`` report.

    ``base.user_admin`` is an automatic member of
    ``school_admission_fee_analysis_group`` (see ``res_group/
    school_admission_fee_analysis.xml``), so no extra group grant is
    needed here for the ``login="admin"`` tour session.
    """

    @classmethod
    def setUpClass(cls):
        """Build one admission with a single non-voided fee line."""
        super().setUpClass()

        cls.admin_user = cls.env.ref("base.user_admin")

        income_type = cls.env.ref("account.data_account_type_revenue")
        cls.income_account = cls.env["account.account"].create(
            {
                "name": "TOUR ADM FEE ANALYSIS Income",
                "code": "TOURADMFAINC",
                "user_type_id": income_type.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {"name": "TOUR ADM FEE ANALYSIS Fee"}
        )
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR ADM FEE ANALYSIS Grade Type", "code": "TOURADMFAGT"}
        )
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ADM FEE ANALYSIS Academic Year",
                "code": "TOURADMFAAY",
                "date_start": "2027-07-01",
                "date_end": "2028-06-30",
            }
        )
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR ADM FEE ANALYSIS Term",
                "code": "TOURADMFAT",
                "date_start": "2027-07-01",
                "date_end": "2028-06-30",
                "year_id": cls.academic_year.id,
                "enrollment_state": "open",
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR ADM FEE ANALYSIS School",
                "code": "TOURADMFASCH",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "TOUR ADM FEE ANALYSIS Grade",
                "code": "TOURADMFAG",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.contact = cls.env["res.partner"].create(
            {"name": "TOUR ADM FEE ANALYSIS Student"}
        )

        # user_id is set explicitly: cls.env runs as SUPERUSER_ID during
        # setUpClass (odoo/tests/common.py), and
        # school_admission_internal_user_rule
        # ([('user_id','=',user.id)], base.group_user) would otherwise
        # hide this fixture from the "admin" tour session.
        cls.admission = cls.env["school_admission"].create(
            {
                "date": "2027-07-01",
                "academic_year_id": cls.academic_year.id,
                "academic_term_id": cls.academic_term.id,
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "student_id": cls.contact.id,
                "currency_id": cls.env.company.currency_id.id,
                "user_id": cls.admin_user.id,
            }
        )
        cls.term = cls.env["school_admission_payment_term"].create(
            {
                "admission_id": cls.admission.id,
                "name": "TOUR ADM FEE ANALYSIS Payment Term",
                "sequence": 10,
            }
        )
        cls.detail = cls.env["school_admission_payment_term_detail"].create(
            {
                "term_id": cls.term.id,
                "product_id": cls.product.id,
                "name": "TOUR ADM FEE ANALYSIS Fee Line",
                "account_id": cls.income_account.id,
                "uom_quantity": 1.0,
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "price_unit": 1_000_000.0,
            }
        )

    def test_analyze(self):
        """IK: docs/school_admission_fee_analysis/01-analyze-admission-fee.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_admission_fee_analysis_analyze",
            login="admin",
        )
