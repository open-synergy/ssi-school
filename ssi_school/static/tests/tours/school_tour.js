// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school.school_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- Flow 1 of every
    // school IK: "Open the School > Configuration > Grade > Schools menu."
    // "Grade" (ssi_school.menu_grade_configuration) is a level-3 grouping
    // menuitem with no action= attribute, so 14.0 renders it as a
    // non-clickable dropdown header without data-menu-xmlid -- there is no
    // step for it (patterns.md skill odoo-development-ui-test §A).
    function openSchoolList() {
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
                content: "Open the Schools menu",
                trigger: '.o_menu_sections [data-menu-xmlid="ssi_school.school_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang, bukan
                // sekadar "ada list di layar" (patterns.md §A).
                content: "Schools list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Schools)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/school/01-create.md
    tour.register(
        "ssi_school_school_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Grade > Schools menu.
            openSchoolList(),
            [
                // ── Flow 2 — Click the New button. (14.0: "Create")
                {
                    content: "Click New",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 3 — Fill in the required fields: Name, Code, Grade
                // Type. Center is defaulted from the current company and
                // Branch is optional, so neither is touched here.
                {
                    content: "Fill in the Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR School Create",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },
                {
                    content: "Select the Grade Type",
                    trigger: ".o_field_many2one[name='grade_type_id'] input",
                    run: "text TOUR School Grade Type",
                },
                {
                    content: "Pick the Grade Type from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR School Grade Type)",
                    in_modal: false,
                },

                // ── Flow 4 — Click Generate Code in the header to
                // automatically assign a code from the configured
                // sequence.template.
                {
                    content: "Click Generate Code",
                    trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    // The record has no id until this button auto-saves it;
                    // the breadcrumb literal "New" going away is the
                    // data-independent proof the save + reload completed
                    // (patterns.md §P). The generated Code value itself is
                    // not asserted -- that is a value check, out of tour
                    // scope.
                    content: "Record is saved by Generate Code",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:not(:contains(New))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 5 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — a new School record is created and
                // active.
                {
                    content: "Record is saved",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR School Create)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school/02-edit.md
    tour.register(
        "ssi_school_school_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Grade > Schools menu.
            openSchoolList(),
            [
                // ── Flow 2 — Find and open the record to edit.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR School Edit) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
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
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 3 — Change the required fields (Name, Code, Grade
                // Type, Center, Branch). Only Name is changed here; Code is
                // left as "/" so Flow 4 (Generate Code) has an effect.
                {
                    content: "Change the Name",
                    trigger: ".o_field_widget[name='name']",
                    run: "text TOUR School Edit Changed",
                },

                // ── Flow 4 — Click Generate Code in the header to assign a
                // code from the configured sequence.template, since the Code
                // field is still "/".
                {
                    content: "Click Generate Code",
                    trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    // The breadcrumb still shows the OLD name until the
                    // implicit auto-save triggered by this object button
                    // completes -- a data-independent proof the save landed
                    // (patterns.md §P), without asserting the generated Code
                    // value itself.
                    content: "Record is saved by Generate Code",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR School Edit Changed)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 5 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 6 — Go back to the Schools list, select the
                // record's checkbox, click Reset code, then click OK to
                // confirm. This resets the Code field back to "/".
                {
                    content: "Click the Schools breadcrumb to return to the list",
                    trigger: ".breadcrumb-item.o_back_button a:contains(Schools)",
                },
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR School Edit Changed) .o_list_record_selector input",
                    run: "click",
                },
                {
                    content: "Click Reset code",
                    trigger: ".o_cp_buttons button[name='action_reset_code']",
                },
                {
                    content: "Confirm reset code",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — the record is updated with the new
                // values.
                {
                    content:
                        "Reset code dialog is closed and the Schools list is displayed",
                    trigger: ".o_list_view",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school/03-delete.md
    tour.register(
        "ssi_school_school_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Grade > Schools menu.
            openSchoolList(),
            [
                // ── Flow 2 — Select one or more records to delete (check the
                // checkbox).
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR School Delete) .o_list_record_selector input",
                    run: "click",
                },

                // ── Flow 3 — Click Action > Delete.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Delete",
                    // Item Action menu adalah komponen Owl; cocokkan LABEL
                    // PERSIS -- :contains(Delete) sebagai substring bisa
                    // keliru menunjuk item lain (patterns.md §I).
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

                // ── Flow 4 — Click OK to confirm.
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — the selected records are permanently
                // removed from the system.
                {
                    content: "Record no longer in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR School Delete)))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school/04-deactivate.md
    tour.register(
        "ssi_school_school_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Grade > Schools menu.
            openSchoolList(),
            [
                // ── Flow 2 — Select one or more records to deactivate (check
                // the checkbox).
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR School Deactivate) .o_list_record_selector input",
                    run: "click",
                },

                // ── Flow 3 — Click Action > Archive.
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

                // ── Flow 4 — Click OK to confirm.
                {
                    content: "Confirm archive",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — the records are archived and no longer
                // appear in the default list view.
                {
                    content: "Record no longer in the default list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR School Deactivate)))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school/05-activate.md
    tour.register(
        "ssi_school_school_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Grade > Schools menu.
            openSchoolList(),
            [
                // ── Flow 2 — Enable the Archived filter in the search bar.
                {
                    content: "Wait for the list data to finish loading",
                    trigger: ".o_list_view .o_data_row",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Open the Filters menu",
                    trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                    run: function () {
                        // Dropdown Owl 14.0 tidak selalu terbuka oleh klik
                        // sintetis default -- pakai klik browser asli
                        // (patterns.md §I box).
                        this.$anchor[0].click();
                    },
                },
                {
                    content: "Enable the Archived filter",
                    trigger: ".o_filter_menu .o_menu_item:contains(Archived) a",
                    run: function () {
                        this.$anchor[0].click();
                    },
                },

                // ── Flow 3 — Select one or more records to reactivate (check
                // the checkbox).
                {
                    content: "Select the archived record's checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR School Activate) .o_list_record_selector input",
                    run: "click",
                },

                // ── Flow 4 — Click Action > Unarchive.
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

                // ── Flow 5 — Click OK to confirm.
                {
                    content: "Confirm unarchive",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — the records are restored and appear
                // again in the default list view. Remove the Archived filter
                // facet to observe the default list.
                {
                    content: "Remove the Archived filter",
                    trigger: ".o_searchview_facet .o_facet_remove",
                    run: "click",
                },
                {
                    content: "Record appears again in the default list",
                    trigger: ".o_data_row:contains(TOUR School Activate)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school/06-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the button opens the
    // "Select Report To Print" wizard, then closes it via Cancel. It never
    // selects a report nor clicks the wizard's own Print button, because the
    // resulting report action is an ir.actions.act_url download with no DOM
    // "finished" signal -- clicking through it could hang headless Chrome.
    tour.register(
        "ssi_school_school_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Grade > Schools menu.
            openSchoolList(),
            [
                // ── Flow 2 — Open the record to print.
                {
                    content: "Open the school record",
                    trigger:
                        ".o_data_row:contains(TOUR PRINT SCHOOL) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "School form is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 3 — Click the Print button.
                // The button is injected by mixin.print_document as
                // type="action" -- its `name` attribute is a numeric action
                // id resolved at render time, so it must be targeted by its
                // visible label (selectors.md §4), not by `[name=...]`.
                {
                    content: "Click the Print button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Print')",
                    extra_trigger: ".o_form_view",
                },

                // ── Flow 4/5 boundary — the wizard is proven open, then
                // closed. Selecting the report and clicking the wizard's own
                // Print button are intentionally NOT executed -- see the
                // module docstring above.
                {
                    content: "The Select Report To Print wizard is displayed",
                    trigger: ".modal-title:contains('Select Report To Print')",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Close the wizard",
                    trigger: ".modal-footer button[special='cancel']",
                    in_modal: true,
                },

                // ── Post-Condition (tour boundary) — the wizard is closed
                // and the school form is displayed again. Whether a report
                // is actually generated and downloaded is out of tour scope.
                {
                    content: "Wizard is closed and the school form is displayed",
                    trigger: ".o_form_view",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );
});
