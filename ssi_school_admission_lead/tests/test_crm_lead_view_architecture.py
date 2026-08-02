# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCrmLeadViewArchitecture(YamlTransactionCase):
    """Python murni — pemicu P1 (L-01: `action: call` membuang nilai balik method).

    Tata letak view (posisi field di dalam sebuah `<group>`) bukan permukaan yang
    dapat diekspresikan DSL `odoo-yaml-test` — tidak ada aksi YAML yang membaca arch
    hasil `fields_view_get`. Regresi ini memanggil `fields_view_get` langsung dan
    memeriksa nilai balik `arch` yang dikembalikan method tersebut.
    """

    def setUp(self):
        super().setUp()
        result = self.env["crm.lead"].fields_view_get(view_type="form")
        self.arch = etree.fromstring(result["arch"])

    def _group(self, name):
        groups = self.arch.xpath("//group[@name='%s']" % name)
        self.assertTrue(groups, "Group '%s' should exist in the form arch" % name)
        return groups[0]

    def test_prospective_student_group_contains_expected_fields_in_order(self):
        group = self._group("school_lead_prospective_student")
        field_names = [f.get("name") for f in group.xpath(".//field")]
        self.assertEqual(
            field_names,
            [
                "student_id",
                "student_birthdate",
                "student_gender",
                "birth_city",
                "religion_id",
                "nationality_id",
                "allowed_previous_school_ids",
                "previous_school_id",
                "student_nickname",
                "student_nisn",
                "parent_relationship",
            ],
            "Prospective Student group should list student_id, student_birthdate, "
            "student_gender, birth_city, religion_id, nationality_id, "
            "allowed_previous_school_ids, previous_school_id, student_nickname, "
            "student_nisn, parent_relationship in that order",
        )
        previous_school_id_field = group.xpath(".//field[@name='previous_school_id']")[
            0
        ]
        self.assertEqual(
            previous_school_id_field.get("domain"),
            "[('id', 'in', allowed_previous_school_ids)]",
            "previous_school_id should be restricted by allowed_previous_school_ids",
        )

    def test_admission_target_group_contains_expected_fields_in_order(self):
        group = self._group("school_lead_admission_target")
        field_names = [f.get("name") for f in group.xpath(".//field")]
        self.assertEqual(
            field_names,
            ["school_id", "grade_type_id", "grade_id"],
            "Admission Target group should list school_id, grade_type_id, "
            "grade_id in that order",
        )
        grade_id_field = group.xpath(".//field[@name='grade_id']")[0]
        self.assertEqual(
            grade_id_field.get("domain"),
            "[('type_id', '=', grade_type_id)]",
            "grade_id should keep its domain filtering by grade_type_id",
        )

    def test_admission_document_group_contains_expected_fields(self):
        group = self._group("school_lead_admission_document")
        field_names = [f.get("name") for f in group.xpath(".//field")]
        self.assertIn("admission_id", field_names)
        self.assertIn("admission_form_id", field_names)
        self.assertIn("admission_test_id", field_names)

    def test_module_specific_thematic_groups_are_removed(self):
        for group_name in (
            "school_admission_lead_student_identity",
            "school_admission_lead_target_grade",
        ):
            groups = self.arch.xpath("//group[@name='%s']" % group_name)
            self.assertFalse(
                groups,
                "Group '%s' should no longer be defined by "
                "ssi_school_admission_lead" % group_name,
            )

    def test_admission_fields_are_not_inserted_into_crm_partner_groups(self):
        for group_name in ("lead_partner", "opportunity_partner"):
            group = self._group(group_name)
            field_names = [f.get("name") for f in group.xpath(".//field")]
            self.assertNotIn(
                "admission_form_id",
                field_names,
                "admission_form_id should not be a child of '%s'" % group_name,
            )
            self.assertNotIn(
                "admission_test_id",
                field_names,
                "admission_test_id should not be a child of '%s'" % group_name,
            )
