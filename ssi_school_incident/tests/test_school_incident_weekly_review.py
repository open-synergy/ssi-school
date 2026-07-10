# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolIncidentWeeklyReview(YamlTransactionCase):
    def test_school_incident_weekly_review(self):
        self.run_yaml_scenario("test_data_school_incident_weekly_review.yaml")

    def _create_minimal_student(self, code_suffix, school=False):
        if not school:
            grade_type = self.env["school_grade_type"].create(
                {
                    "name": "Grade Type Weekly Review OC %s" % code_suffix,
                    "code": "GTWROC%s" % code_suffix,
                }
            )
            school = self.env["school"].create(
                {
                    "name": "School Weekly Review OC %s" % code_suffix,
                    "code": "SCHWROC%s" % code_suffix,
                    "grade_type_id": grade_type.id,
                }
            )
        contact = self.env["res.partner"].create(
            {"name": "Student Contact Weekly Review OC %s" % code_suffix}
        )
        student = self.env["school_student"].create(
            {
                "name": "Student Weekly Review OC %s" % code_suffix,
                "code": "STUWROC%s" % code_suffix,
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        return student, school

    def _create_incident_type(self, code_suffix):
        return self.env["school_incident_type"].create(
            {
                "name": "Incident Type Weekly Review OC %s" % code_suffix,
                "code": "INCTYPE-WR-OC-%s" % code_suffix,
            }
        )

    def _create_incident(
        self,
        student,
        incident_type,
        date_incident,
        resolution_status="in_progress",
        handling_level="1",
        date_resolved=False,
        date_first_contact=False,
    ):
        vals = {
            "date_incident": date_incident,
            "student_id": student.id,
            "incident_type_id": incident_type.id,
            "handling_level": handling_level,
            "description": "Weekly Review test case.",
            "resolution_status": resolution_status,
        }
        if date_resolved:
            vals["date_resolved"] = date_resolved
        if date_first_contact:
            vals["date_first_contact"] = date_first_contact
        return self.env["school_incident"].create(vals)

    def test_collect_incidents_filters_by_school_and_date_range(self):
        """action_collect_incidents must only pull in School Incidents
        whose Incident Date falls within [date_start, date_end] AND
        (when School is set) whose Student belongs to that School."""
        student_1, school_1 = self._create_minimal_student("10")
        student_2, _school_2 = self._create_minimal_student("11")
        incident_type = self._create_incident_type("10")

        today = date.today()
        date_start = today - timedelta(days=15)
        date_end = today

        in_range_same_school = self._create_incident(
            student_1, incident_type, today - timedelta(days=5)
        )
        out_of_range_same_school = self._create_incident(
            student_1, incident_type, today - timedelta(days=60)
        )
        in_range_other_school = self._create_incident(
            student_2, incident_type, today - timedelta(days=3)
        )

        review = self.env["school_incident_weekly_review"].create(
            {
                "school_id": school_1.id,
                "date_start": date_start,
                "date_end": date_end,
            }
        )
        review.action_collect_incidents()

        self.assertEqual(review.incident_ids, in_range_same_school)
        self.assertNotIn(out_of_range_same_school, review.incident_ids)
        self.assertNotIn(in_range_other_school, review.incident_ids)
        self.assertEqual(review.count_total, 1)

    def test_collect_incidents_without_school_includes_all_schools(self):
        """When school_id is empty, _get_incident_criteria must not add a
        school filter, so incidents from any School within the date
        range are collected."""
        student_1, _school_1 = self._create_minimal_student("12")
        student_2, _school_2 = self._create_minimal_student("13")
        incident_type = self._create_incident_type("11")

        today = date.today()
        date_start = today - timedelta(days=15)
        date_end = today

        incident_school_1 = self._create_incident(
            student_1, incident_type, today - timedelta(days=5)
        )
        incident_school_2 = self._create_incident(
            student_2, incident_type, today - timedelta(days=3)
        )
        out_of_range = self._create_incident(
            student_1, incident_type, today - timedelta(days=60)
        )

        review = self.env["school_incident_weekly_review"].create(
            {
                "date_start": date_start,
                "date_end": date_end,
            }
        )
        review.action_collect_incidents()

        self.assertIn(incident_school_1, review.incident_ids)
        self.assertIn(incident_school_2, review.incident_ids)
        self.assertNotIn(out_of_range, review.incident_ids)
        self.assertEqual(review.count_total, 2)

    def test_compute_counts_overdue_escalated_unresolved_over_7d(self):
        """count_overdue/count_escalated/count_unresolved_over_7d must
        match the underlying school_incident data once collected."""
        student, school = self._create_minimal_student("14")
        incident_type = self._create_incident_type("12")

        today = date.today()
        date_start = today - timedelta(days=15)
        date_end = today

        # Overdue + still unresolved beyond 7 days: no first contact, no
        # resolution recorded, incident date far enough in the past that
        # both the First Contact and Resolution SLA (tier 1: 24h/24h)
        # have long since passed.
        not_resolved_overdue = self._create_incident(
            student,
            incident_type,
            today - timedelta(days=10),
            resolution_status="not_resolved",
            handling_level="1",
        )
        # Escalated and overdue (tier 3 resolution SLA is 168h/7 days;
        # 10 days ago is already past that), but must NOT be counted as
        # "unresolved over 7 days" since it is already escalated.
        escalated_overdue = self._create_incident(
            student,
            incident_type,
            today - timedelta(days=10),
            resolution_status="escalated",
            handling_level="3",
        )
        # Resolved well within SLA: first contact same day, resolved same
        # day -> must not be counted as overdue nor as unresolved.
        resolved_on_time = self._create_incident(
            student,
            incident_type,
            today - timedelta(days=10),
            resolution_status="resolved_satisfied",
            handling_level="1",
            date_resolved=today - timedelta(days=9),
            date_first_contact=today - timedelta(days=10),
        )
        # Out of the review's date range entirely -- must never be
        # collected, so it cannot pollute any of the counts.
        self._create_incident(
            student,
            incident_type,
            today - timedelta(days=60),
            resolution_status="not_resolved",
        )

        review = self.env["school_incident_weekly_review"].create(
            {
                "school_id": school.id,
                "date_start": date_start,
                "date_end": date_end,
            }
        )
        review.action_collect_incidents()

        self.assertEqual(review.count_total, 3)
        self.assertIn(not_resolved_overdue, review.incident_ids)
        self.assertIn(escalated_overdue, review.incident_ids)
        self.assertIn(resolved_on_time, review.incident_ids)

        self.assertEqual(review.count_overdue, 2)
        self.assertEqual(review.count_escalated, 1)
        self.assertEqual(review.count_unresolved_over_7d, 1)
