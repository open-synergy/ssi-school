# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolAcademicTermAdmission(HttpSavepointCase):
    """UI/UX delta tour tests for ``school_academic_term``.

    Covers only the ``is_open_admission`` field this module adds to the
    base ``ssi_school`` model (E1 archetype -- see
    ``odoo-development-ui-test`` ``scope-and-boundaries.md`` §3). Each
    ``test_*`` method runs the tour pairing with the delta IK file named
    in its docstring (``docs/school_academic_term/NN-*.md``); navigation
    itself is sourced from the base module's own IK, per the "Backing
    dua-file" rule.
    """

    @classmethod
    def setUpClass(cls):
        """Create the Academic Year and the Draft term used by 02-edit."""
        super().setUpClass()

        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ADM TERM Academic Year",
                "code": "TOURADMTY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        # 02-edit.md -- a record to open and edit.
        cls.term_edit = cls.env["school_academic_term"].create(
            {
                "name": "TOUR ADM TERM Edit",
                "code": "TOURADMTE",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": cls.academic_year.id,
            }
        )

    def test_create(self):
        """IK: docs/school_academic_term/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_academic_term_create",
            login="admin",
        )

    def test_edit(self):
        """IK: docs/school_academic_term/02-edit.md"""
        self.start_tour(
            "/web",
            "ssi_school_admission_school_academic_term_edit",
            login="admin",
        )
