# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import ValidationError
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentMutation(YamlTransactionCase):
    def test_school_student_mutation(self):
        self.run_yaml_scenario("test_data_school_student_mutation.yaml")

    def _setup_open_enrollment(self, suffix):
        """Create grade type/school/grade/two grade classes/year/term/
        student and an enrollment already brought to open state, ready
        to be used as the base fixture for a class mutation test."""
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type Mutation %s" % suffix,
                "code": "GTSM%s" % suffix,
                "sequence": 10,
            }
        )
        school = self.env["school"].create(
            {
                "name": "School Mutation %s" % suffix,
                "code": "SCHSM%s" % suffix,
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Mutation %s" % suffix,
                "code": "GSM%s" % suffix,
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class_a = self.env["school_grade_class"].create(
            {
                "name": "Class A Mutation %s" % suffix,
                "code": "CLSM%sA" % suffix,
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        grade_class_b = self.env["school_grade_class"].create(
            {
                "name": "Class B Mutation %s" % suffix,
                "code": "CLSM%sB" % suffix,
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        year = self.env["school_academic_year"].create(
            {
                "name": "Year Mutation %s" % suffix,
                "code": "AYSM%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = self.env["school_academic_term"].create(
            {
                "name": "Term Mutation %s" % suffix,
                "code": "TMSM%s" % suffix,
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Contact Mutation %s" % suffix}
        )
        student = self.env["school_student"].create(
            {
                "name": "Student Mutation %s" % suffix,
                "code": "STUSM%s" % suffix,
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        enrollment = self.env["school_enrollment"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": year.id,
                "academic_term_id": term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class_a.id,
                "student_id": student.id,
                "currency_id": self.env.company.currency_id.id,
            }
        )
        admin = self.env.ref("base.user_admin")
        enrollment.with_user(admin).action_confirm()
        enrollment.with_user(admin).action_approve_approval()
        self.assertEqual(enrollment.state, "open")
        return {
            "grade_type": grade_type,
            "school": school,
            "grade": grade,
            "grade_class_a": grade_class_a,
            "grade_class_b": grade_class_b,
            "year": year,
            "term": term,
            "student": student,
            "enrollment": enrollment,
        }

    def test_onchange_enrollment_id_from_student_id(self):
        """Setting student_id must auto-fill enrollment_id from the
        student's active_enrollment_id."""
        data = self._setup_open_enrollment("O1")
        form = Form(self.env["school_student_mutation"])
        form.student_id = data["student"]
        self.assertEqual(form.enrollment_id, data["enrollment"])

    def test_onchange_source_snapshot_from_enrollment_id(self):
        """Selecting the enrollment must snapshot source_grade_class_id
        and source_homeroom_id from the enrollment, chained from
        student_id."""
        data = self._setup_open_enrollment("O2")
        homeroom = self.env["school_homeroom"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": data["year"].id,
                "academic_term_id": data["term"].id,
                "school_id": data["school"].id,
                "grade_id": data["grade"].id,
                "grade_class_id": data["grade_class_a"].id,
                "capacity": 30,
            }
        )
        data["enrollment"].write({"homeroom_id": homeroom.id})

        form = Form(self.env["school_student_mutation"])
        form.student_id = data["student"]
        self.assertEqual(form.source_grade_class_id, data["grade_class_a"])
        self.assertEqual(form.source_homeroom_id, homeroom)

    def test_onchange_destination_homeroom_id_from_destination_grade_class_id(self):
        """Selecting destination_grade_class_id must auto-search and
        fill destination_homeroom_id from an open Homeroom batch."""
        data = self._setup_open_enrollment("O3")
        homeroom_b = self.env["school_homeroom"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": data["year"].id,
                "academic_term_id": data["term"].id,
                "school_id": data["school"].id,
                "grade_id": data["grade"].id,
                "grade_class_id": data["grade_class_b"].id,
                "capacity": 30,
            }
        )
        admin = self.env.ref("base.user_admin")
        homeroom_b.with_user(admin).action_confirm()
        homeroom_b.with_user(admin).action_approve_approval()
        self.assertEqual(homeroom_b.state, "open")

        form = Form(self.env["school_student_mutation"])
        form.student_id = data["student"]
        form.destination_grade_class_id = data["grade_class_b"]
        self.assertEqual(form.destination_homeroom_id, homeroom_b)

    def test_constrain_destination_must_differ_from_source(self):
        """destination_grade_class_id equal to the enrollment's
        current grade class must be rejected."""
        data = self._setup_open_enrollment("D1")
        with self.assertRaises(ValidationError):
            self.env["school_student_mutation"].create(
                {
                    "date": "2024-07-01",
                    "student_id": data["student"].id,
                    "enrollment_id": data["enrollment"].id,
                    "destination_grade_class_id": data["grade_class_a"].id,
                }
            )

    def test_constrain_destination_must_match_grade_school(self):
        """destination_grade_class_id from a different grade must be
        rejected."""
        data = self._setup_open_enrollment("D2")
        other_grade = self.env["school_grade"].create(
            {
                "name": "Other Grade Mutation D2",
                "code": "GSMD2B",
                "sequence": 20,
                "type_id": data["grade_type"].id,
            }
        )
        other_class = self.env["school_grade_class"].create(
            {
                "name": "Other Class Mutation D2",
                "code": "CLSMD2C",
                "school_id": data["school"].id,
                "grade_id": other_grade.id,
                "capacity": 30,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["school_student_mutation"].create(
                {
                    "date": "2024-07-01",
                    "student_id": data["student"].id,
                    "enrollment_id": data["enrollment"].id,
                    "destination_grade_class_id": other_class.id,
                }
            )

    def test_constrain_enrollment_must_be_open_to_confirm(self):
        """Confirming a mutation whose enrollment is no longer open
        must be rejected."""
        data = self._setup_open_enrollment("E1")
        mutation = self.env["school_student_mutation"].create(
            {
                "date": "2024-07-01",
                "student_id": data["student"].id,
                "enrollment_id": data["enrollment"].id,
                "destination_grade_class_id": data["grade_class_b"].id,
            }
        )
        data["enrollment"].with_context(bypass_policy_check=True).action_cancel()
        with self.assertRaises(ValidationError):
            mutation.write({"state": "confirm"})

    def test_constrain_single_active_mutation_for_same_enrollment(self):
        """Only one draft/confirm mutation is allowed per enrollment at
        a time."""
        data = self._setup_open_enrollment("M1")
        self.env["school_student_mutation"].create(
            {
                "date": "2024-07-01",
                "student_id": data["student"].id,
                "enrollment_id": data["enrollment"].id,
                "destination_grade_class_id": data["grade_class_b"].id,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["school_student_mutation"].create(
                {
                    "date": "2024-07-01",
                    "student_id": data["student"].id,
                    "enrollment_id": data["enrollment"].id,
                    "destination_grade_class_id": data["grade_class_b"].id,
                }
            )

    def test_constrain_quota_full_blocks_done(self):
        """Completing a mutation into a full-capacity destination
        class must be rejected and leave the enrollment untouched."""
        data = self._setup_open_enrollment("Q1")
        data["grade_class_b"].write({"capacity": 1})

        filler_contact = self.env["res.partner"].create(
            {"name": "Filler Contact Mutation Q1"}
        )
        filler_student = self.env["school_student"].create(
            {
                "name": "Filler Student Mutation Q1",
                "code": "STUSMQ1F",
                "contact_id": filler_contact.id,
                "school_id": data["school"].id,
            }
        )
        filler_enrollment = self.env["school_enrollment"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": data["year"].id,
                "academic_term_id": data["term"].id,
                "school_id": data["school"].id,
                "grade_id": data["grade"].id,
                "grade_class_id": data["grade_class_b"].id,
                "student_id": filler_student.id,
                "currency_id": self.env.company.currency_id.id,
            }
        )
        admin = self.env.ref("base.user_admin")
        filler_enrollment.with_user(admin).action_confirm()
        filler_enrollment.with_user(admin).action_approve_approval()
        self.assertEqual(filler_enrollment.state, "open")

        mutation = self.env["school_student_mutation"].create(
            {
                "date": "2024-07-01",
                "student_id": data["student"].id,
                "enrollment_id": data["enrollment"].id,
                "destination_grade_class_id": data["grade_class_b"].id,
            }
        )
        mutation.with_user(admin).action_confirm()
        self.assertEqual(mutation.state, "confirm")

        with self.assertRaises(ValidationError):
            mutation.with_user(admin).action_approve_approval()

        self.assertEqual(mutation.state, "confirm")
        self.assertEqual(data["enrollment"].grade_class_id, data["grade_class_a"])
