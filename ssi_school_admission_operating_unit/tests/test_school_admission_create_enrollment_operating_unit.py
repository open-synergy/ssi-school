# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionCreateEnrollmentOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover operating unit propagation on the Create Enrollment wizard.

    Includes the win over school-derived/user-default operating units,
    idempotency on a repeated wizard call, and admissions without an
    operating unit.
    """

    def test_school_admission_create_enrollment_operating_unit(self):
        """Run every Create Enrollment wizard operating unit scenario."""
        self.run_yaml_scenario(
            "test_data_school_admission_create_enrollment_operating_unit.yaml"
        )
