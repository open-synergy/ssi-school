# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentCreateInvoiceExport(YamlTransactionCase):
    """Cover ``school_enrollment.wizard_create_invoice_export``.

    Exercises both the YAML behavior scenario (wizard action) and the
    Python-only wizard form arch assertions below.
    """

    def test_school_enrollment_create_invoice_export(self):
        """Run the create-invoice-export wizard scenario."""
        self.run_yaml_scenario("test_data_enrollment_create_invoice_export.yaml")

    def test_enrollment_ids_field_is_invisible_without_widget(self):
        """Assert the source field is hidden but stays in the arch.

        Pure Python test, trigger P1 (L-01/L-02): the arch dict returned
        by ``fields_view_get()`` is not a surface the ``odoo-yaml-test``
        DSL can read (``action: call`` discards the return value), and
        the YAML ``assert`` block only supports dotted ``getattr`` on
        registry records, never expressions over the view arch XML.

        ``enrollment_ids`` must stay in the wizard form arch as a
        machine-only field (``invisible="1"``), without
        ``widget="many2many_tags"``.
        """
        model = self.env["school_enrollment.wizard_create_invoice_export"]
        result = model.fields_view_get(view_type="form")
        arch = etree.fromstring(result["arch"])

        field = arch.find(".//field[@name='enrollment_ids']")
        self.assertIsNotNone(field, "enrollment_ids field not found in arch")
        self.assertEqual(field.get("invisible"), "1")
        self.assertIsNone(
            field.get("widget"),
            "enrollment_ids should no longer carry widget=many2many_tags",
        )

    def test_required_fields_are_not_invisible(self):
        """Assert the user-fillable fields are not hidden.

        Pure Python test, trigger P1 (L-01/L-02): same rationale as
        ``test_enrollment_ids_field_is_invisible_without_widget`` above
        — the view arch is only inspectable via ``fields_view_get()``.

        ``type_id``, ``date``, ``output_format``, ``date_start`` and
        ``date_end`` must stay visible (no ``invisible`` attribute) on
        the wizard form.
        """
        model = self.env["school_enrollment.wizard_create_invoice_export"]
        result = model.fields_view_get(view_type="form")
        arch = etree.fromstring(result["arch"])

        for field_name in (
            "type_id",
            "date",
            "output_format",
            "date_start",
            "date_end",
        ):
            field = arch.find(".//field[@name='%s']" % field_name)
            self.assertIsNotNone(field, "%s field not found in arch" % field_name)
            self.assertIsNone(
                field.get("invisible"),
                "%s should not be invisible" % field_name,
            )
