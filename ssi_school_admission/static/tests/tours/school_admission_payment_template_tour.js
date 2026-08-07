// Copyright 2024 OpenSynergy Indonesia
// Copyright 2024 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_admission.school_admission_payment_template_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared navigation block -- corresponds to Flow 1 of every
        // school_admission_payment_template IK: "Open the School >
        // Configuration > Admission > Payment Templates menu."
        // "Admission" (menu_admission_configuration) is a level-3+
        // grouping menuitem with no action -> non-clickable header, no
        // step for it (patterns.md §A).
        function openPaymentTemplateList() {
            return [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Configuration menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_configuration"]',
                },
                {
                    content: "Open the Payment Templates menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_admission.school_admission_payment_template_menu"]',
                },
                {
                    content: "Payment Templates list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Templates)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },
            ];
        }

        // IK: docs/school_admission_payment_template/01-create.md
        tour.register(
            "ssi_school_admission_school_admission_payment_template_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openPaymentTemplateList(),
                [
                    // Flow 2 -- Click New. (14.0: "Create")
                    {
                        content: "Click New",
                        trigger: ".o_list_button_add",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open in edit mode",
                        trigger: ".o_form_view.o_form_editable",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 3 -- Fill in the required fields: Name, Code.
                    // Academic Term, School, Grade are optional and left
                    // at their defaults.
                    {
                        content: "Fill in the Name",
                        trigger: ".o_field_widget[name='name']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOUR ADM PMT TPL CREATE",
                    },
                    {
                        content: "Fill in the Code",
                        trigger: ".o_field_widget[name='code']",
                        run: "text /",
                    },

                    // Flow 4 -- On the Payment Terms tab, add one term
                    // with one fee detail line. term_ids/detail_ids are
                    // declared with a <tree>+<form> combo and no
                    // editable= attribute, so "Add a line" opens a
                    // FormViewDialog rather than an inline row (verified
                    // against web/static/src/js/fields/
                    // relational_fields.js `_onAddRecord`).
                    {
                        content: "Open the Payment Terms tab",
                        trigger: ".o_notebook .nav-link:contains(Payment Terms)",
                    },
                    {
                        content: "Click Add a line on the Payment Terms table",
                        trigger:
                            ".o_field_widget[name='term_ids'] .o_field_x2many_list_row_add a",
                    },
                    {
                        // 14.0: JANGAN prefiks `.modal` (patterns.md §H).
                        content: "The term dialog is displayed",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        // The "text" run helper only dispatches synthetic
                        // keydown/keyup, never a real `input` event --
                        // harmless normally (Save re-reads the raw
                        // input), but adding the nested detail_ids row a
                        // few steps below re-renders this dialog's own
                        // form and can wipe an uncommitted value.
                        // Dispatch real input/change events so the
                        // debounced commit fires immediately.
                        content: "Fill in the Term Name",
                        trigger: ".o_field_widget[name='name']",
                        run: function () {
                            var el = this.$anchor[0];
                            el.value = "TOUR ADM PMT Term 1";
                            el.dispatchEvent(new InputEvent("input", {bubbles: true}));
                            el.dispatchEvent(new Event("change", {bubbles: true}));
                        },
                    },
                    // Flow 4 -- Invoice Date Duration / Due Date Duration
                    // are left empty (IK: "Leave a duration field empty
                    // to skip auto-computing").
                    {
                        content: "Open the Detail tab in the term dialog",
                        trigger: ".o_notebook .nav-link:contains(Detail)",
                    },
                    {
                        content: "Click Add a line on the Detail table",
                        trigger:
                            ".o_field_widget[name='detail_ids'] .o_field_x2many_list_row_add a",
                    },
                    {
                        // A second, nested FormViewDialog opens on top of
                        // the term dialog; $modal_displayed now resolves
                        // to this innermost modal.
                        content: "The detail line dialog is displayed",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        // Selecting Product is enough: onchange_name and
                        // onchange_account_id
                        // (school_admission_payment_template_term_detail.py)
                        // auto-fill Name and Account from the product
                        // (property_account_income_id set in setUpClass).
                        content: "Select the Product",
                        trigger: ".o_field_many2one[name='product_id'] input",
                        run: "text TOUR ADM PMT TPL PRODUCT",
                    },
                    {
                        content: "Pick the Product from the dropdown",
                        trigger:
                            ".ui-autocomplete .ui-menu-item a:contains(TOUR ADM PMT TPL PRODUCT)",
                        in_modal: false,
                    },
                    {
                        content: "Save & Close the detail line dialog",
                        trigger: ".modal-footer button.btn-primary",
                        in_modal: true,
                    },
                    {
                        // Gerbang: back to a single modal (the term
                        // dialog) -- the detail dialog's own root is
                        // gone.
                        content: "Detail line dialog is closed",
                        trigger: ".o_field_widget[name='detail_ids'] .o_data_row",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        // Defensive backstop: the nested detail_ids row
                        // re-renders the term dialog's own form and can
                        // wipe the Name input's value even after it was
                        // committed earlier. Re-fill immediately before
                        // Save.
                        content: "Re-confirm the Term Name before saving",
                        trigger: ".o_field_widget[name='name']",
                        run: function () {
                            var el = this.$anchor[0];
                            el.value = "TOUR ADM PMT Term 1";
                            el.dispatchEvent(new InputEvent("input", {bubbles: true}));
                            el.dispatchEvent(new Event("change", {bubbles: true}));
                        },
                    },
                    {
                        content: "Save & Close the term dialog",
                        trigger: ".modal-footer button.btn-primary",
                        in_modal: true,
                    },
                    {
                        content: "Term dialog is closed",
                        trigger:
                            ".o_field_widget[name='term_ids'] .o_data_row:contains(TOUR ADM PMT Term 1)",
                        extra_trigger: "body:not(:has(.modal))",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 5 -- Product Configuration tab keeps its
                    // Domain default (only the tab render is verified).
                    {
                        content: "Open the Product Configuration tab",
                        trigger: ".o_notebook .nav-link:contains(Product Configuration)",
                    },
                    {
                        content: "Product Configuration tab is displayed",
                        trigger: ".o_field_widget[name='product_selection_method']",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 6 -- On the Accounting tab, select the
                    // required Customer Invoice Type.
                    {
                        content: "Open the Accounting tab",
                        trigger: ".o_notebook .nav-link:contains(Accounting)",
                    },
                    {
                        content: "Select the Customer Invoice Type",
                        trigger:
                            ".o_field_many2one[name='customer_invoice_type_id'] input",
                        run: "text TOUR ADM PMT TPL INVOICE TYPE CREATE",
                    },
                    {
                        content: "Pick the Customer Invoice Type from the dropdown",
                        trigger:
                            ".ui-autocomplete .ui-menu-item a:contains(TOUR ADM PMT TPL INVOICE TYPE CREATE)",
                        in_modal: false,
                    },

                    // Flow 7 -- Click Generate Code in the header.
                    {
                        content: "Click Generate Code",
                        trigger:
                            ".o_statusbar_buttons button[name='action_generate_code']",
                        extra_trigger: ".o_form_view",
                    },
                    {
                        content: "Generate Code call has completed",
                        trigger:
                            ".o_statusbar_buttons button[name='action_generate_code']:enabled",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 8 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },
                    {
                        content: "Record is saved and displayed",
                        trigger: ".o_form_view.o_form_readonly",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_admission_payment_template/02-edit.md
        tour.register(
            "ssi_school_admission_school_admission_payment_template_edit",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openPaymentTemplateList(),
                [
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR ADM PMT TPL EDIT) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Click the Edit button",
                        trigger: ".o_form_button_edit",
                    },
                    {
                        content: "Form is now editable",
                        trigger: ".o_form_view.o_form_editable",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 3 -- Change the required fields.
                    {
                        content: "Change the Name",
                        trigger: ".o_field_widget[name='name']",
                        run: "text TOUR ADM PMT TPL EDIT CHANGED",
                    },

                    // Flow 5 -- Click Generate Code (Code still "/").
                    {
                        content: "Click Generate Code",
                        trigger:
                            ".o_statusbar_buttons button[name='action_generate_code']",
                        extra_trigger: ".o_form_view.o_form_editable",
                    },
                    {
                        content: "Generate Code call has completed",
                        trigger:
                            ".o_statusbar_buttons button[name='action_generate_code']:enabled",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 6 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },
                    {
                        content: "Record is saved",
                        trigger: ".o_form_view.o_form_readonly",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 7 -- Reset code.
                    {
                        content: "Click the Payment Templates breadcrumb",
                        trigger:
                            ".breadcrumb-item.o_back_button a:contains(Payment Templates)",
                    },
                    {
                        content: "Select the record's checkbox",
                        trigger:
                            ".o_data_row:contains(TOUR ADM PMT TPL EDIT CHANGED) .o_list_record_selector input",
                        run: "click",
                    },
                    {
                        content: "Click Reset code in the list toolbar",
                        trigger: ".o_cp_buttons button[name='action_reset_code']",
                    },
                    {
                        content: "Reset Code completes (row selection cleared)",
                        trigger:
                            ".o_data_row:contains(TOUR ADM PMT TPL EDIT CHANGED) .o_list_record_selector input:not(:checked)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_admission_payment_template/03-delete.md
        tour.register(
            "ssi_school_admission_school_admission_payment_template_delete",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openPaymentTemplateList(),
                [
                    {
                        content: "Select the record to delete",
                        trigger:
                            ".o_data_row:contains(TOUR ADM PMT TPL DELETE) .o_list_record_selector input",
                        run: "click",
                    },
                    {
                        content: "Open the Action menu",
                        trigger: ".o_cp_action_menus button:contains(Action)",
                    },
                    {
                        content: "Click Delete",
                        trigger: ".o_cp_action_menus .o_menu_item a",
                        run: function () {
                            var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                                function () {
                                    return $(this).text().trim() === "Delete";
                                }
                            );
                            $delete[0].click();
                        },
                    },
                    {
                        content: "Confirm deletion",
                        trigger: ".modal-footer button.btn-primary",
                        in_modal: true,
                    },
                    {
                        content: "Record no longer appears in the list",
                        trigger:
                            ".o_list_view:not(:has(.o_data_row:contains(TOUR ADM PMT TPL DELETE)))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_admission_payment_template/04-deactivate.md
        tour.register(
            "ssi_school_admission_school_admission_payment_template_deactivate",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openPaymentTemplateList(),
                [
                    {
                        content: "Select the record to deactivate",
                        trigger:
                            ".o_data_row:contains(TOUR ADM PMT TPL DEACTIVATE) .o_list_record_selector input",
                        run: "click",
                    },
                    {
                        content: "Open the Action menu",
                        trigger: ".o_cp_action_menus button:contains(Action)",
                    },
                    {
                        content: "Click Archive",
                        trigger: ".o_cp_action_menus .o_menu_item a",
                        run: function () {
                            var $archive = $(".o_cp_action_menus .o_menu_item a").filter(
                                function () {
                                    return $(this).text().trim() === "Archive";
                                }
                            );
                            $archive[0].click();
                        },
                    },
                    {
                        content: "Confirm the dialog",
                        trigger: ".modal-footer button.btn-primary",
                        in_modal: true,
                    },
                    {
                        content: "Record no longer appears in the active list",
                        trigger:
                            ".o_list_view:not(:has(.o_data_row:contains(TOUR ADM PMT TPL DEACTIVATE)))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_admission_payment_template/05-activate.md
        tour.register(
            "ssi_school_admission_school_admission_payment_template_activate",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openPaymentTemplateList(),
                [
                    {
                        content: "Open the Filters menu",
                        trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                        run: function () {
                            this.$anchor[0].click();
                        },
                    },
                    {
                        content: "Enable the Archived filter",
                        trigger: ".o_filter_menu .o_menu_item a:contains(Archived)",
                        run: function () {
                            this.$anchor[0].click();
                        },
                    },
                    {
                        content: "Select the record to reactivate",
                        trigger:
                            ".o_data_row:contains(TOUR ADM PMT TPL ACTIVATE) .o_list_record_selector input",
                        run: "click",
                    },
                    {
                        content: "Open the Action menu",
                        trigger: ".o_cp_action_menus button:contains(Action)",
                    },
                    {
                        content: "Click Unarchive",
                        trigger: ".o_cp_action_menus .o_menu_item a",
                        run: function () {
                            var $unarchive = $(
                                ".o_cp_action_menus .o_menu_item a"
                            ).filter(function () {
                                return $(this).text().trim() === "Unarchive";
                            });
                            $unarchive[0].click();
                        },
                    },
                    {
                        content: "Unarchive completes (row leaves the Archived list)",
                        trigger:
                            ".o_list_view:not(:has(.o_data_row:contains(TOUR ADM PMT TPL ACTIVATE)))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Open the Filters menu again",
                        trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                        run: function () {
                            this.$anchor[0].click();
                        },
                    },
                    {
                        content: "Disable the Archived filter",
                        trigger: ".o_filter_menu .o_menu_item a:contains(Archived)",
                        run: function () {
                            this.$anchor[0].click();
                        },
                    },
                    {
                        content: "Record appears again in the active list",
                        trigger: ".o_data_row:contains(TOUR ADM PMT TPL ACTIVATE)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_admission_payment_template/06-print.md
        tour.register(
            "ssi_school_admission_school_admission_payment_template_print",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openPaymentTemplateList(),
                [
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR ADM PMT TPL PRINT) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is displayed",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Click the Print button",
                        trigger: ".o_statusbar_buttons button:enabled:contains('Print')",
                        extra_trigger: ".o_form_view",
                    },
                    {
                        content: "The Select Report To Print wizard is displayed",
                        trigger: ".modal-title:contains('Select Report To Print')",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Close the wizard",
                        trigger: ".modal-footer button[special='cancel']",
                        in_modal: true,
                    },
                    {
                        content: "Wizard is closed and the form is displayed again",
                        trigger: ".o_form_view",
                        extra_trigger: "body:not(:has(.modal))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
