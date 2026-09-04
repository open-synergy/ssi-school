# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionPaymentTermPaid(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``paid`` value of an admission payment term.

    The scenarios exercise the invoice-driven ``paid`` state: a term
    that follows its linked customer invoice to ``done`` and back to
    ``open``, a manually controlled term without a customer invoice
    that never becomes ``paid``, and a cancelled admission that keeps
    its term ``cancelled`` even when the linked invoice is ``done``.
    """

    def test_admission_payment_term_paid(self):
        """Run the paid-state and its negative-path scenarios."""
        self.run_yaml_scenario("test_data_admission_payment_term_paid.yaml")
