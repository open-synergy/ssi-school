# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolStudentStates(YamlTransactionCase):
    """Cover the state transitions of ``school_student``.

    The scenarios drive a student into each of its terminal states,
    check the transitions the guard in ``write`` forbids, and replay the
    legal two step reactivation of a dropped student through draft.
    """

    def test_student_states(self):
        """Run the scenarios driving a student into each state."""
        self.run_yaml_scenario("test_data_student_states.yaml")
