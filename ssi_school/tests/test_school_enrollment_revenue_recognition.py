# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentRevenueRecognition(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the enrollment Revenue Recognition feature end to end.

    The scenarios exercise: the ``final_usage_id``/``final_account_id``
    onchange on a payment term detail, copying that pair from the
    payment template on ``action_compute_payment``, posting the
    Revenue Recognition move on Done (including a negative-amount
    detail's debit/credit swap and skipping uninvoiced/final-account-
    less details), leaving the move empty while the flag is disabled,
    enabling the flag on an already-open enrollment, a due invoice
    created after Done billing straight to the Final Account,
    rejecting the cancellation of an already-recognized invoice,
    deleting the move when a recognized enrollment is cancelled, the
    addendum lock rejecting a write on an invoiced detail, and the
    Done readiness checks (draft invoice, missing journal).
    """

    def test_enrollment_revenue_recognition(self):
        """Run every Revenue Recognition scenario against the fixtures."""
        self.run_yaml_scenario("test_data_enrollment_revenue_recognition.yaml")
