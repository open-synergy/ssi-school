# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCrmLeadStudentNickname(YamlTransactionCase):
    """Test the ``student_nickname`` related field on ``crm.lead``."""

    def test_crm_lead_student_nickname(self):
        """Run the YAML scenarios covering ``student_nickname`` sync."""
        self.run_yaml_scenario("test_data_crm_lead_student_nickname.yaml")

    def test_student_nickname_is_not_readonly(self):
        """Python murni — pemicu P1 (L-01: `fields_get()` mengembalikan dict,

        YAML tidak bisa meng-assert nilai balik method).

        Related field ``store=True`` bawaan Odoo di-set ``readonly=True``
        secara default (``odoo/fields.py`` - ``Field._setup_attrs``); test
        ini memverifikasi ``student_nickname`` sudah diberi
        ``readonly=False`` eksplisit sehingga dapat diedit dari form
        ``crm.lead``.
        """
        fields_info = self.env["crm.lead"].fields_get(["student_nickname"])
        self.assertFalse(
            fields_info["student_nickname"]["readonly"],
            "Field student_nickname should not be readonly",
        )
