# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchool(YamlTransactionCase):
    def test_school(self):
        self.run_yaml_scenario("test_data_school.yaml")

    def test_onchange_branch_id_clears_on_company_change(self):
        """Mengganti company_id harus mengosongkan branch_id bila branch
        yang terpilih tidak lagi berada di bawah company baru."""
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Branch Onchange", "code": "GTBOC", "sequence": 10}
        )
        other_company = self.env["res.company"].create({"name": "Other Center"})
        branch = self.env["school_branch"].create(
            {
                "name": "Branch Onchange",
                "code": "BROC",
                "company_id": self.env.company.id,
            }
        )
        form = Form(self.env["school"])
        form.name = "School Onchange Branch"
        form.code = "SCHOCB"
        form.grade_type_id = grade_type
        form.branch_id = branch
        form.company_id = other_company
        self.assertFalse(form.branch_id._origin)  # pylint: disable=protected-access
