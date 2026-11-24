# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase

from odoo.modules import get_module_path
from odoo.tests import tagged

MODULE = "ssi_school"
VERSION = "14.0.5.22.0"


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentLockMigration(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the post-migrate script that locks open/done enrollments.

    The script of version ``14.0.5.22.0`` locks every payment term and
    detail line that is still unlocked and belongs to an enrollment in
    state ``open`` or ``done``, and leaves draft enrollments alone.
    """

    def _load_script(self):
        """Load ``post-migrate.py`` of the target version from disk.

        :return: the loaded script module exposing ``migrate``
        """
        path = os.path.join(
            get_module_path(MODULE),
            "migrations",
            VERSION,
            "post-migrate.py",
        )
        spec = importlib.util.spec_from_file_location("post_migrate_lock", path)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        return script

    def _locked_flags(self, term, detail):
        """Read the ``locked`` flags straight from the database.

        :param term: the payment term under test
        :param detail: the detail line under test
        :return: tuple ``(term_locked, detail_locked)``
        """
        self.env.cr.execute(
            "SELECT locked FROM school_enrollment_payment_term WHERE id = %s",
            (term.id,),
        )
        term_locked = self.env.cr.fetchone()[0]
        self.env.cr.execute(
            "SELECT locked FROM school_enrollment_payment_term_detail " "WHERE id = %s",
            (detail.id,),
        )
        detail_locked = self.env.cr.fetchone()[0]
        return term_locked, detail_locked

    def _set_state(self, enrollment, term, detail, state):
        """Force an enrollment state and unlock its term and detail.

        :param enrollment: the enrollment to update
        :param term: its payment term, reset to unlocked
        :param detail: its detail line, reset to unlocked
        :param state: the state written with plain SQL
        :return: None
        """
        cr = self.env.cr
        cr.execute(
            "UPDATE school_enrollment SET state = %s WHERE id = %s",
            (state, enrollment.id),
        )
        cr.execute(
            "UPDATE school_enrollment_payment_term SET locked = false " "WHERE id = %s",
            (term.id,),
        )
        cr.execute(
            "UPDATE school_enrollment_payment_term_detail SET locked = false "
            "WHERE id = %s",
            (detail.id,),
        )

    def test_post_migrate_locks_open_and_done(self):
        """Lock open and done enrollments, skip draft ones.

        Pure Python test (``P10``, ``L-11``): the migration script has to
        be imported from its file, which ``EVAL:`` cannot do. The YAML
        scenario only builds the draft fixture; the states are then
        forced with SQL so the script runs on each of them in turn.
        """
        self.run_yaml_scenario("test_data_enrollment_lock_migration.yaml")
        term = self.env["school_enrollment_payment_term"].search(
            [("name", "=", "Term 1 MIGLK1")]
        )
        detail = term.detail_ids
        enrollment = term.enrollment_id
        self.assertEqual(len(term), 1)
        self.assertEqual(len(detail), 1)
        self.env["school_enrollment_payment_term_detail"].flush()
        script = self._load_script()

        self._set_state(enrollment, term, detail, "draft")
        script.migrate(self.env.cr, VERSION)
        self.assertEqual(self._locked_flags(term, detail), (False, False))

        self._set_state(enrollment, term, detail, "open")
        script.migrate(self.env.cr, VERSION)
        self.assertEqual(self._locked_flags(term, detail), (True, True))

        self._set_state(enrollment, term, detail, "done")
        script.migrate(self.env.cr, VERSION)
        self.assertEqual(self._locked_flags(term, detail), (True, True))
