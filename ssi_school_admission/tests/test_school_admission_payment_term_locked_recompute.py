# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAdmissionPaymentTermLockedRecompute(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover recomputing ``state`` on an already-locked payment term.

    The scenarios reproduce the 2026-09-04 production deploy failure
    of the twin module ``ssi_school`` (issue #387): calling
    ``_compute_state()`` directly on a ``locked`` term must not raise,
    since ``Field.compute_value`` writes it at the field level under
    ``env.protecting`` rather than through the model's ``write()``.
    The negative scenario proves the addendum lock still rejects a
    mixed write that combines ``state`` with a field outside
    ``ADDENDUM_LOCK_ALLOWED_FIELDS``.
    """

    def test_admission_payment_term_locked_recompute(self):
        """Run the locked-recompute scenarios."""
        self.run_yaml_scenario("test_data_admission_payment_term_locked_recompute.yaml")
