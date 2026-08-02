# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolQrCode(YamlTransactionCase):
    """Scenario tests for ``school_student`` with ``mixin.qr_code``.

    ``ssi_school_qr_code`` ships no QR configuration data on purpose:
    the QR content is configured ad hoc per deployment on the
    ``ir.model`` row of ``school_student``. The scenarios therefore
    configure that row themselves and cover the unconfigured,
    standard-content, custom-content, and broken-custom-content
    paths of ``qr_image``.
    """

    def test_school_qr_code(self):
        """Run the ``qr_image`` and master data scenarios.

        :return: nothing; assertions live in the YAML scenarios
        """
        self.run_yaml_scenario("test_data_school_qr_code.yaml")
