# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolHomeroom(YamlTransactionCase):
    def test_school_homeroom(self):
        self.run_yaml_scenario("test_data_school_homeroom.yaml")

    def test_onchange_capacity_from_grade_class_id(self):
        """Setting grade_class_id must fill capacity from its capacity."""
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Homeroom Onchange", "code": "GTHRO", "sequence": 10}
        )
        school = self.env["school"].create(
            {
                "name": "School Homeroom Onchange",
                "code": "SCHHRO",
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Homeroom Onchange",
                "code": "GHRO",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class Homeroom Onchange",
                "code": "CLHRO",
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 25,
            }
        )
        year = self.env["school_academic_year"].create(
            {
                "name": "Year Homeroom Onchange",
                "code": "AYHRO",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = self.env["school_academic_term"].create(
            {
                "name": "Term Homeroom Onchange",
                "code": "TMHRO",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )

        form = Form(self.env["school_homeroom"])
        form.academic_year_id = year
        form.academic_term_id = term
        form.school_id = school
        form.grade_id = grade
        form.grade_class_id = grade_class
        self.assertEqual(form.capacity, 25)

    def test_fill_random_only_picks_allowed_students(self):
        """Fill Random must only pick from allowed_student_ids, never a
        student excluded by state, school, or grade mismatch."""
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Fill Random 1", "code": "GTFR1", "sequence": 10}
        )
        school = self.env["school"].create(
            {
                "name": "School Fill Random 1",
                "code": "SCHFR1",
                "grade_type_id": grade_type.id,
            }
        )
        other_school = self.env["school"].create(
            {
                "name": "Other School Fill Random 1",
                "code": "SCHFR1B",
                "grade_type_id": grade_type.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Fill Random 1",
                "code": "GFR1",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        other_grade = self.env["school_grade"].create(
            {
                "name": "Other Grade Fill Random 1",
                "code": "GFR1B",
                "sequence": 20,
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class Fill Random 1",
                "code": "CLFR1",
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 50,
            }
        )
        year = self.env["school_academic_year"].create(
            {
                "name": "Year Fill Random 1",
                "code": "AYFR1",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term_1 = self.env["school_academic_term"].create(
            {
                "name": "Term 1 Fill Random 1",
                "code": "TMFR1A",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
            }
        )
        term_2 = self.env["school_academic_term"].create(
            {
                "name": "Term 2 Fill Random 1",
                "code": "TMFR1B",
                "date_start": "2025-01-01",
                "date_end": "2025-06-30",
                "year_id": year.id,
            }
        )
        self.assertTrue(term_1.first_term)
        self.assertFalse(term_2.first_term)

        def make_student(code, school_id, initial_grade_id):
            contact = self.env["res.partner"].create({"name": "Contact %s" % code})
            return self.env["school_student"].create(
                {
                    "name": "Student %s" % code,
                    "code": code,
                    "contact_id": contact.id,
                    "school_id": school_id,
                    "initial_grade_id": initial_grade_id,
                }
            )

        student_1 = make_student("STUFR1A", school.id, grade.id)
        student_2 = make_student("STUFR1B", school.id, grade.id)
        student_3 = make_student("STUFR1C", school.id, grade.id)
        allowed_students = student_1 | student_2 | student_3
        non_draft_student = make_student("STUFR1D", school.id, grade.id)
        non_draft_student.write({"state": "enrol"})
        other_school_student = make_student("STUFR1E", other_school.id, grade.id)
        other_grade_student = make_student("STUFR1F", school.id, other_grade.id)

        homeroom = self.env["school_homeroom"].create(
            {
                "date": "2025-01-01",
                "academic_year_id": year.id,
                "academic_term_id": term_2.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "capacity": 50,
            }
        )
        homeroom.action_fill_random()

        self.assertEqual(homeroom.candidate_student_ids, allowed_students)
        self.assertNotIn(non_draft_student, homeroom.candidate_student_ids)
        self.assertNotIn(other_school_student, homeroom.candidate_student_ids)
        self.assertNotIn(other_grade_student, homeroom.candidate_student_ids)

    def test_fill_random_first_term_uses_next_grade(self):
        """On the first term of an academic year, Fill Random must select
        students whose next_grade_id matches the homeroom grade, mirroring
        school_enrollment's allowed_student_ids algorithm."""
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Fill Random 2", "code": "GTFR2", "sequence": 10}
        )
        school = self.env["school"].create(
            {
                "name": "School Fill Random 2",
                "code": "SCHFR2",
                "grade_type_id": grade_type.id,
            }
        )
        grade_prev = self.env["school_grade"].create(
            {
                "name": "Grade Prev Fill Random 2",
                "code": "GFR2A",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_target = self.env["school_grade"].create(
            {
                "name": "Grade Target Fill Random 2",
                "code": "GFR2B",
                "sequence": 20,
                "type_id": grade_type.id,
            }
        )
        self.assertEqual(grade_prev.next_grade_id, grade_target)
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class Fill Random 2",
                "code": "CLFR2",
                "school_id": school.id,
                "grade_id": grade_target.id,
                "capacity": 50,
            }
        )
        year = self.env["school_academic_year"].create(
            {
                "name": "Year Fill Random 2",
                "code": "AYFR2",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term = self.env["school_academic_term"].create(
            {
                "name": "Term Fill Random 2",
                "code": "TMFR2",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
                "year_id": year.id,
            }
        )
        self.assertTrue(term.first_term)

        contact_a = self.env["res.partner"].create({"name": "Contact FR2 A"})
        student_a = self.env["school_student"].create(
            {
                "name": "Student FR2 A",
                "code": "STUFR2A",
                "contact_id": contact_a.id,
                "school_id": school.id,
                "initial_grade_id": grade_prev.id,
            }
        )
        self.assertEqual(student_a.next_grade_id, grade_target)

        contact_b = self.env["res.partner"].create({"name": "Contact FR2 B"})
        student_b = self.env["school_student"].create(
            {
                "name": "Student FR2 B",
                "code": "STUFR2B",
                "contact_id": contact_b.id,
                "school_id": school.id,
                "initial_grade_id": grade_target.id,
            }
        )
        self.assertEqual(student_b.current_grade_id, grade_target)
        self.assertNotEqual(student_b.next_grade_id, grade_target)

        homeroom = self.env["school_homeroom"].create(
            {
                "date": "2024-07-01",
                "academic_year_id": year.id,
                "academic_term_id": term.id,
                "school_id": school.id,
                "grade_id": grade_target.id,
                "grade_class_id": grade_class.id,
                "capacity": 50,
            }
        )
        homeroom.action_fill_random()

        self.assertIn(student_a, homeroom.candidate_student_ids)
        self.assertNotIn(student_b, homeroom.candidate_student_ids)

    def test_fill_random_non_first_term_uses_current_grade(self):
        """On a non-first term of an academic year, Fill Random must select
        students whose current_grade_id matches the homeroom grade, mirroring
        school_enrollment's allowed_student_ids algorithm."""
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Fill Random 3", "code": "GTFR3", "sequence": 10}
        )
        school = self.env["school"].create(
            {
                "name": "School Fill Random 3",
                "code": "SCHFR3",
                "grade_type_id": grade_type.id,
            }
        )
        grade_prev = self.env["school_grade"].create(
            {
                "name": "Grade Prev Fill Random 3",
                "code": "GFR3A",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_target = self.env["school_grade"].create(
            {
                "name": "Grade Target Fill Random 3",
                "code": "GFR3B",
                "sequence": 20,
                "type_id": grade_type.id,
            }
        )
        self.assertEqual(grade_prev.next_grade_id, grade_target)
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Class Fill Random 3",
                "code": "CLFR3",
                "school_id": school.id,
                "grade_id": grade_target.id,
                "capacity": 50,
            }
        )
        year = self.env["school_academic_year"].create(
            {
                "name": "Year Fill Random 3",
                "code": "AYFR3",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        term_1 = self.env["school_academic_term"].create(
            {
                "name": "Term 1 Fill Random 3",
                "code": "TMFR3A",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": year.id,
            }
        )
        term_2 = self.env["school_academic_term"].create(
            {
                "name": "Term 2 Fill Random 3",
                "code": "TMFR3B",
                "date_start": "2025-01-01",
                "date_end": "2025-06-30",
                "year_id": year.id,
            }
        )
        self.assertTrue(term_1.first_term)
        self.assertFalse(term_2.first_term)

        contact_a = self.env["res.partner"].create({"name": "Contact FR3 A"})
        student_a = self.env["school_student"].create(
            {
                "name": "Student FR3 A",
                "code": "STUFR3A",
                "contact_id": contact_a.id,
                "school_id": school.id,
                "initial_grade_id": grade_target.id,
            }
        )
        self.assertEqual(student_a.current_grade_id, grade_target)

        contact_b = self.env["res.partner"].create({"name": "Contact FR3 B"})
        student_b = self.env["school_student"].create(
            {
                "name": "Student FR3 B",
                "code": "STUFR3B",
                "contact_id": contact_b.id,
                "school_id": school.id,
                "initial_grade_id": grade_prev.id,
            }
        )
        self.assertEqual(student_b.next_grade_id, grade_target)
        self.assertNotEqual(student_b.current_grade_id, grade_target)

        homeroom = self.env["school_homeroom"].create(
            {
                "date": "2025-01-01",
                "academic_year_id": year.id,
                "academic_term_id": term_2.id,
                "school_id": school.id,
                "grade_id": grade_target.id,
                "grade_class_id": grade_class.id,
                "capacity": 50,
            }
        )
        homeroom.action_fill_random()

        self.assertIn(student_a, homeroom.candidate_student_ids)
        self.assertNotIn(student_b, homeroom.candidate_student_ids)
