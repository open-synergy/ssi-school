# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCrmLeadParentContact(YamlTransactionCase):
    def test_crm_lead_parent_contact(self):
        self.run_yaml_scenario("test_data_crm_lead_parent_contact.yaml")

    def test_parent_fields_are_not_readonly(self):
        """Python murni — pemicu P1 (L-01: `fields_get()` mengembalikan dict,

        YAML tidak bisa meng-assert nilai balik method).

        Related field ``store=True`` bawaan Odoo di-set ``readonly=True``
        secara default (``odoo/fields.py`` - ``Field._setup_attrs``); test
        ini memverifikasi kesembilan field ``parent_*`` sudah diberi
        ``readonly=False`` eksplisit sehingga dapat diedit dari form
        ``crm.lead``.
        """
        fields_info = self.env["crm.lead"].fields_get(
            [
                "parent_street",
                "parent_street2",
                "parent_city",
                "parent_state_id",
                "parent_zip",
                "parent_country_id",
                "parent_phone",
                "parent_mobile",
                "parent_email",
            ]
        )
        for field_name, field_info in fields_info.items():
            self.assertFalse(
                field_info["readonly"],
                "Field %s should not be readonly" % field_name,
            )
