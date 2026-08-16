# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCrmLeadCreateAdmissionOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Test operating unit propagation from ``crm.lead`` to admission.

    Covers both admission creation wizards opened from a lead
    (``crm.lead.create_admission_form`` and ``crm.lead.create_admission``):
    the wizard must default ``operating_unit_id`` from the originating
    lead, and the resulting admission document must carry that same
    operating unit.
    """

    def test_crm_lead_create_admission_operating_unit(self):
        """Run the lead-to-admission operating unit propagation scenarios.

        Asserts that the admission form and the admission created from a
        lead inherit ``operating_unit_id`` from that lead.
        """
        self.run_yaml_scenario(
            "test_data_crm_lead_create_admission_operating_unit.yaml"
        )
