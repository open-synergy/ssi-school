# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolHealth(YamlTransactionCase):
    """Cover the ``school_student`` health fields and their history lines.

    Exercises the related One2many fields (height, weight, head
    circumference, allergy, disease history) exposed on
    ``school_student`` through the linked ``res.partner`` contact.
    """

    def test_school_health(self):
        """Run the school health scenario."""
        self.run_yaml_scenario("test_data_school_health.yaml")


@tagged("post_install", "-at_install")
class TestSchoolHealthAccess(YamlTransactionCase):
    """Cover the access rules of the ``Student Health`` group.

    The YAML scenario covers the group definition and the read/write
    behaviour of the health data. The Python methods cover the view
    arch and the menu visibility, which YAML cannot assert.
    """

    def setUp(self):
        """Create the student record and the two users used by the tests."""
        super().setUp()
        grade_type = self.env["school_grade_type"].create(
            {"name": "PY Health Grade Type", "code": "PYHGT", "sequence": 10}
        )
        school = self.env["school"].create(
            {
                "name": "PY Health School",
                "code": "PYHSCH",
                "grade_type_id": grade_type.id,
            }
        )
        contact = self.env["res.partner"].create({"name": "PY Health Contact"})
        self.student = self.env["school_student"].create(
            {
                "name": "PY Health Student",
                "code": "PYHSTU",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        base_user = self.env.ref("base.group_user")
        self.user_student = self._create_user(
            "py_health_student",
            base_user + self.env.ref("ssi_school.school_student_group"),
        )
        self.user_health = self._create_user(
            "py_health_health",
            base_user + self.env.ref("ssi_school_health.school_student_health_group"),
        )

    def _create_user(self, login, groups):
        """Create an internal user that belongs to exactly ``groups``.

        :param login: Login (and name) of the new user.
        :param groups: ``res.groups`` recordset to assign.
        :return: The created ``res.users`` record.
        """
        return self.env["res.users"].create(
            {
                "name": login,
                "login": login,
                "password": "Sch00l-Health-Access-2026!",
                "groups_id": [(6, 0, groups.ids)],
            }
        )

    def _get_form_arch(self, user):
        """Return the parsed student form arch and fields as ``user``.

        :param user: ``res.users`` record used to read the view.
        :return: Tuple of the parsed arch root and the fields dict.
        """
        view = self.env.ref("ssi_school.school_student_view_form")
        result = (
            self.env["school_student"]
            .with_user(user)
            .fields_view_get(view_id=view.id, view_type="form")
        )
        return etree.fromstring(result["arch"]), result["fields"]

    def test_access(self):
        """Run the Student Health group access scenario."""
        self.run_yaml_scenario("test_data_school_health_access.yaml")

    def test_health_page_hidden_for_student_user(self):
        """Assert the Health page is invisible for a Student-only user.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards the
        return value of ``fields_view_get``, so YAML cannot assert it).
        """
        arch, fields = self._get_form_arch(self.user_student)
        pages = arch.xpath("//page[@name='health']")
        self.assertEqual(len(pages), 1)
        self.assertIn('"invisible": true', pages[0].get("modifiers"))
        self.assertFalse(arch.xpath("//field[@name='allergy_ids']"))
        # Reading every field of the arch must not raise AccessError.
        self.student.with_user(self.user_student).read(list(fields))

    def test_health_page_visible_for_health_user(self):
        """Assert the Health page is visible for a Student Health user.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards the
        return value of ``fields_view_get``, so YAML cannot assert it).
        """
        arch, fields = self._get_form_arch(self.user_health)
        pages = arch.xpath("//page[@name='health']")
        self.assertEqual(len(pages), 1)
        self.assertNotIn('"invisible": true', pages[0].get("modifiers") or "")
        self.assertTrue(arch.xpath("//field[@name='allergy_ids']"))
        self.student.with_user(self.user_health).read(list(fields))

    def test_contacts_menu_hidden_for_health_user(self):
        """Assert the Contacts menu stays hidden for a Student Health user.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards the
        return value of ``_visible_menu_ids``, so YAML cannot assert it).
        """
        menu = self.env.ref("contacts.res_partner_menu_contacts")
        visible = self.env["ir.ui.menu"].with_user(self.user_health)
        self.assertNotIn(menu.id, visible._visible_menu_ids())
        configurator = self.env.ref("ssi_partner.contacts_configurator_group")
        self.assertNotIn(configurator, self.user_health.groups_id)
