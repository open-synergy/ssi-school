// Copyright 2022 OpenSynergy Indonesia
// Copyright 2022 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_admission.school_admission_fee_template_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- corresponds to Flow 1 of every
    // school_admission_fee_template IK: "Open the School > Configuration
    // > Admission > Fee Templates menu." "Configuration" is a level-2
    // section WITH children -> clickable dropdown-toggle. "Admission"
    // (menu_admission_configuration, ssi_school/menu.xml) is a level-3+
    // grouping menuitem with NO action -> non-clickable header, no step
    // for it; its children (including "Fee Templates") are flattened
    // into the same Configuration dropdown (patterns.md §A).
    function openFeeTemplateList() {
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
                content: "Open the Fee Templates menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_admission.school_admission_fee_template_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang
                // (patterns.md §A).
                content: "Fee Templates list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Fee Templates)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    }

    // IK: docs/school_admission_fee_template/01-create.md
    tour.register(
        "ssi_school_admission_school_admission_fee_template_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openFeeTemplateList(), [
            // Flow 2 -- Click the New button. (14.0: "Create")
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
            // School, Grade, Journal, and Account are optional and
            // left at their defaults.
            {
                content: "Fill in the Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR ADM FEE TPL CREATE",
            },
            {
                content: "Fill in the Code",
                trigger: ".o_field_widget[name='code']",
                run: "text /",
            },

            // Flow 4 -- On the Fee Lines tab, add one line.
            {
                content: "Open the Fee Lines tab",
                trigger: ".o_notebook .nav-link:contains(Fee Lines)",
            },
            {
                content: "Add a line",
                trigger:
                    ".o_field_widget[name='line_ids'] .o_field_x2many_list_row_add a",
            },
            {
                content: "Select the Product",
                trigger: ".o_selected_row .o_field_widget[name='product_id'] input",
                run: "text TOUR ADM FEE TPL PRODUCT",
            },
            {
                content: "Pick the Product from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR ADM FEE TPL PRODUCT)",
                in_modal: false,
            },
            {
                content: "Select the Account",
                trigger: ".o_selected_row .o_field_widget[name='account_id'] input",
                run: "text TOUR ADM FEE TPL INCOME",
            },
            {
                content: "Pick the Account from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR ADM FEE TPL INCOME)",
                in_modal: false,
            },
            {
                // Commit the last edited cell -- never `press Tab`
                // (patterns.md §C). Click an already-committed cell
                // on the same row to blur.
                content: "Commit the fee line",
                trigger: ".o_selected_row .o_field_widget[name='product_id']",
                run: "click",
            },

            // Flow 5 -- Click Generate Code in the header.
            {
                content: "Click Generate Code",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                extra_trigger: ".o_form_view",
            },
            {
                // Gerbang: tombol object di-disable sinkron sampai
                // siklus auto-save + call_button + reload selesai
                // (patterns.md §P).
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
        ])
    );

    // IK: docs/school_admission_fee_template/02-edit.md
    tour.register(
        "ssi_school_admission_school_admission_fee_template_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openFeeTemplateList(), [
            // Flow 2 -- Find and open the record to edit.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR ADM FEE TPL EDIT) .o_data_cell:first",
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
                run: "text TOUR ADM FEE TPL EDIT CHANGED",
            },

            // Flow 5 -- Click Generate Code in the header (Code is
            // still "/", set by setUpClass).
            {
                content: "Click Generate Code",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
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

            // Flow 7 -- Reset code: back to the list, select the
            // record, click Reset code, then OK.
            {
                content: "Click the Fee Templates breadcrumb",
                trigger: ".breadcrumb-item.o_back_button a:contains(Fee Templates)",
            },
            {
                content: "Select the record's checkbox",
                trigger:
                    ".o_data_row:contains(TOUR ADM FEE TPL EDIT CHANGED) .o_list_record_selector input",
                run: "click",
            },
            {
                content: "Click Reset code in the list toolbar",
                trigger: ".o_cp_buttons button[name='action_reset_code']",
            },
            {
                // 14.0 list-header bulk buttons never read `confirm=`
                // (only form/kanban controllers do) -- the RPC fires
                // immediately and the row selection clears on
                // reload, a data-independent proof it landed.
                content: "Reset Code completes (row selection cleared)",
                trigger:
                    ".o_data_row:contains(TOUR ADM FEE TPL EDIT CHANGED) .o_list_record_selector input:not(:checked)",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/school_admission_fee_template/03-delete.md
    tour.register(
        "ssi_school_admission_school_admission_fee_template_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openFeeTemplateList(), [
            // Flow 2 -- Select the record to delete.
            {
                content: "Select the record to delete",
                trigger:
                    ".o_data_row:contains(TOUR ADM FEE TPL DELETE) .o_list_record_selector input",
                run: "click",
            },

            // Flow 3 -- Click Action > Delete.
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                // Match the exact label (patterns.md §I).
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

            // Flow 4 -- Click OK to confirm.
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition.
            {
                content: "Record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR ADM FEE TPL DELETE)))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/school_admission_fee_template/04-deactivate.md
    tour.register(
        "ssi_school_admission_school_admission_fee_template_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openFeeTemplateList(), [
            {
                content: "Select the record to deactivate",
                trigger:
                    ".o_data_row:contains(TOUR ADM FEE TPL DEACTIVATE) .o_list_record_selector input",
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
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR ADM FEE TPL DEACTIVATE)))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/school_admission_fee_template/05-activate.md
    tour.register(
        "ssi_school_admission_school_admission_fee_template_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openFeeTemplateList(), [
            {
                content: "Open the Filters menu",
                trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                run: function () {
                    // Owl dropdown tidak selalu terbuka oleh klik
                    // sintetis default (patterns.md §I/§J).
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
                    ".o_data_row:contains(TOUR ADM FEE TPL ACTIVATE) .o_list_record_selector input",
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
                    var $unarchive = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Unarchive";
                        }
                    );
                    $unarchive[0].click();
                },
            },
            // No dialog step: Unarchive fires immediately in 14.0
            // core (list_controller.js), only Archive wraps
            // Dialog.confirm(...) -- known IK inaccuracy.
            {
                content: "Unarchive completes (row leaves the Archived list)",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR ADM FEE TPL ACTIVATE)))",
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
                trigger: ".o_data_row:contains(TOUR ADM FEE TPL ACTIVATE)",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/school_admission_fee_template/06-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the button opens
    // the "Select Report To Print" wizard, then closes it via Cancel.
    tour.register(
        "ssi_school_admission_school_admission_fee_template_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(openFeeTemplateList(), [
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR ADM FEE TPL PRINT) .o_data_cell:first",
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
                // Injected by ssi_print_mixin as type="action" --
                // targeted by visible label, not [name=...]
                // (selectors.md §4).
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
        ])
    );
});
