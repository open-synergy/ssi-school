// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_customer_invoice_export.school_enrollment_create_invoice_export_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared navigation block -- corresponds to Flow 1 of the IK:
        // "Open the School > Student Activities > Enrollments menu."
        // Mirrors ssi_school.school_enrollment_tour's own helper.
        function openEnrollmentList() {
            return [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Enrollments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.school_enrollment_menu"]',
                },
                {
                    // Gerbang: tunggu action TUJUAN benar-benar terpasang.
                    content: "Enrollments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Enrollments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ];
        }

        // Opens the record identified by the unique student name shown on
        // the list row's Student column.
        function openRecordByStudent(studentName) {
            return [
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(" + studentName + ") .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
            ];
        }

        // IK: docs/school_enrollment/23-create-invoice-export.md
        tour.register(
            "ssi_school_customer_invoice_export_school_enrollment_create_invoice_export",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Enrollments menu.
                openEnrollmentList(),
                // Flow 2 -- Open the record whose unpaid invoices will be
                // exported.
                openRecordByStudent("TOUR ENR IE Student"),
                [
                    // Flow 3 -- Click the Create Invoice Export button
                    // (action_open_create_invoice_export_wizard).
                    {
                        content: "Click the Create Invoice Export button",
                        trigger:
                            ".o_statusbar_buttons button[name='action_open_create_invoice_export_wizard']",
                        extra_trigger: ".o_form_view",
                    },
                    {
                        // 14.0: JANGAN prefiks `.modal` (patterns.md §H).
                        content: "Wizard is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 4 -- the current record is pre-selected
                    // (Enrollments field, readonly many2many tags, hidden
                    // -- no interaction needed).

                    // Flow 5 -- fill in the required Type field. Date
                    // keeps its default (today), Output Format is
                    // auto-filled from Type, and Date Start/Date End are
                    // left empty (no bound).
                    {
                        content: "Select the Type field value",
                        trigger: ".o_field_many2one[name='type_id'] input",
                        run: "text TOUR ENR IE Export Type",
                    },
                    {
                        content: "Pick the Type from the dropdown",
                        trigger:
                            ".ui-autocomplete .ui-menu-item a:contains(TOUR ENR IE Export Type)",
                        in_modal: false,
                    },

                    // Flow 6 -- Click Create Invoice Export in the wizard
                    // footer.
                    {
                        content: "Click Create Invoice Export in the wizard",
                        trigger:
                            ".modal-footer button[name='action_create_invoice_export']",
                    },
                    {
                        content: "Wizard is closed",
                        trigger: "body:not(:has(.modal))",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Post-Condition -- the created Customer Invoice
                    // Export document opens in form view, in Draft
                    // status. The OLD enrollment form's active statusbar
                    // button is "open", never "draft", so this selector
                    // cannot match before the new document actually
                    // loads (patterns.md §M litmus test).
                    {
                        content:
                            "Customer Invoice Export document opens in Draft status",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
