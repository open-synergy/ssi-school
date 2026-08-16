# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolHealth(YamlTransactionCase):
    """Test the health data a student reads from its linked contact.

    Health measurements and health history are stored on the contact
    (``res.partner``) and surfaced on ``school_student``. This class
    covers both directions: records created through the student must
    land on the contact, and the values reported by the student must
    follow whichever contact it is currently linked to.
    """

    def test_school_health(self):
        """Test student health measurements, history and constraints.

        Runs the YAML scenarios that create height, weight and head
        circumference measurements through ``school_student`` and
        assert that the most recent measurement is the one reported,
        that allergy and disease history entries reflect on the
        contact, that relinking the student to another contact changes
        the reported health values, and that a zero height, a duplicate
        allergen and a recovery date earlier than the diagnosis date
        are all rejected.
        """
        self.run_yaml_scenario("test_data_school_health.yaml")
