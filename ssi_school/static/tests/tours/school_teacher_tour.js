// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school.school_teacher_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- corresponds
    // to Flow 1 of every school_teacher IK: "Open the School > Teachers
    // menu." "Teachers" is a direct child of the School app root
    // (menu_school_root) with no children of its own, so it renders as
    // a single clickable navbar entry -- there is no Configuration step
    // in between.
    function openTeacherList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the School app",
                trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
            },
            {
                content: "Open the Teachers menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.school_teacher_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang,
                // bukan sekadar "ada list di layar" (patterns.md §A).
                content: "Teachers list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Teachers)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/school_teacher/01-create.md
    tour.register(
        "ssi_school_school_teacher_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Teachers menu.
            openTeacherList(),
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
                        // Assertion only.
                    },
                },

                // ── Flow 3 — Fill in the required fields: Name, Code,
                // Employee.
                {
                    content: "Fill in the Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR TEACHER CREATE",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },
                {
                    content: "Select the Employee",
                    trigger: ".o_field_many2one[name='employee_id'] input",
                    run: "text TOUR TEACHER EMPLOYEE CREATE",
                },
                {
                    content: "Pick the Employee from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR TEACHER EMPLOYEE CREATE)",
                    in_modal: false,
                },

                // ── Flow 4 — On the Personal Information tab, review or
                // fill in the identity, birth place, health, and
                // socio-cultural fields synchronized from the employee's
                // Home Address (optional -- none of these fields are
                // required to save, so only the tab render is
                // verified).
                {
                    content: "Open the Personal Information tab",
                    trigger: ".o_notebook .nav-link:contains(Personal Information)",
                },
                {
                    content: "Personal Information tab is displayed",
                    trigger: ".o_field_widget[name='gender']",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Flow 5 — On the Contact & Address tab, review or
                // fill in the address and contact fields (optional --
                // only the tab render is verified).
                {
                    content: "Open the Contact & Address tab",
                    trigger: ".o_notebook .nav-link:contains(Contact & Address)",
                },
                {
                    content: "Contact & Address tab is displayed",
                    trigger: ".o_field_widget[name='phone']",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Flow 6 — On the Bank Accounts tab, add lines as
                // needed (optional -- only the tab render is verified;
                // no line is required to save the record).
                {
                    content: "Open the Bank Accounts tab",
                    trigger: ".o_notebook .nav-link:contains(Bank Accounts)",
                },
                {
                    content: "Bank Accounts tab is displayed",
                    trigger:
                        ".o_field_widget[name='bank_ids'] .o_field_x2many_list_row_add a",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Flow 7 — Click Generate Code in the header.
                {
                    content: "Click Generate Code",
                    trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                    extra_trigger: ".o_form_view",
                },
                {
                    // Gerbang: tombol object di-disable SINKRON saat
                    // diklik dan baru di-enable lagi setelah siklus
                    // auto-save + call_button + reload selesai
                    // (patterns.md §P).
                    content: "Generate Code call has completed",
                    trigger:
                        ".o_statusbar_buttons button[name='action_generate_code']:enabled",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Flow 8 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — A new Teacher record is created
                // and active.
                {
                    content: "Teacher record is saved and displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR TEACHER CREATE)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_teacher/02-edit.md
    tour.register(
        "ssi_school_school_teacher_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Teachers menu.
            openTeacherList(),
            [
                // ── Flow 2 — Find and open the record to edit.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR TEACHER EDIT) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
                // 14.0: an existing record opens read-only -- Edit first
                // (patterns.md skill odoo-development-ui-test §E).
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

                // ── Flow 3 — Change the required fields.
                {
                    content: "Change the Name",
                    trigger: ".o_field_widget[name='name']",
                    run: "text TOUR TEACHER EDIT CHANGED",
                },

                // ── Flow 4 — Update Personal Information, Contact &
                // Address, or Bank Accounts fields as needed (optional
                // -- not exercised here, see the create tour above for
                // the tab-render coverage).

                // ── Flow 5 — Click Generate Code in the header, since
                // the Code field is still "/" (set by setUpClass).
                {
                    content: "Click Generate Code",
                    trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    // Gerbang -- lihat catatan gerbang di tour create
                    // di atas.
                    content: "Generate Code call has completed",
                    trigger:
                        ".o_statusbar_buttons button[name='action_generate_code']:enabled",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Flow 6 — Click Save.
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

                // ── Flow 7 — To make the record eligible for Generate
                // Code again: go back to the Teachers list, select the
                // record's checkbox, click Reset code in the header,
                // then click OK to confirm.
                {
                    content: "Click the Teachers breadcrumb",
                    trigger: ".breadcrumb-item.o_back_button a:contains(Teachers)",
                },
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR TEACHER EDIT CHANGED) .o_list_record_selector input",
                    run: "click",
                },
                {
                    content: "Click Reset code in the list toolbar",
                    trigger: ".o_cp_buttons button[name='action_reset_code']",
                },
                {
                    content: "Click OK to confirm",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — The record is updated with the
                // new values.
                {
                    content: "Reset code dialog is closed",
                    trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_teacher/03-delete.md
    tour.register(
        "ssi_school_school_teacher_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Teachers menu.
            openTeacherList(),
            [
                // ── Flow 2 — Select one or more records to delete
                // (check the checkbox).
                {
                    content: "Select the record to delete",
                    trigger:
                        ".o_data_row:contains(TOUR TEACHER DELETE) .o_list_record_selector input",
                    run: "click",
                },

                // ── Flow 3 — Click Action > Delete.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Delete",
                    // Item Action menu adalah komponen Owl; cocokkan
                    // LABEL PERSIS (patterns.md §I).
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

                // ── Post-Condition — The selected records are
                // permanently removed from the system. The linked
                // hr.employee record itself is not deleted (not a
                // kasatmata UI fact here -- out of tour scope).
                {
                    content: "Record no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR TEACHER DELETE)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_teacher/04-deactivate.md
    tour.register(
        "ssi_school_school_teacher_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Teachers menu.
            openTeacherList(),
            [
                // ── Flow 2 — Select one or more records to deactivate
                // (check the checkbox).
                {
                    content: "Select the record to deactivate",
                    trigger:
                        ".o_data_row:contains(TOUR TEACHER DEACTIVATE) .o_list_record_selector input",
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
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — The records are archived and no
                // longer appear in the default list view.
                {
                    content: "Record no longer appears in the active list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR TEACHER DEACTIVATE)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_teacher/05-activate.md
    tour.register(
        "ssi_school_school_teacher_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Teachers menu.
            openTeacherList(),
            [
                // ── Flow 2 — Enable the Archived filter in the search
                // bar.
                {
                    content: "Open the Filters menu",
                    trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                    run: function () {
                        // Dropdown Owl 14.0 tidak selalu terbuka oleh
                        // klik sintetis default (patterns.md §I/§J).
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

                // ── Flow 3 — Select one or more records to reactivate
                // (check the checkbox).
                {
                    content: "Select the record to reactivate",
                    trigger:
                        ".o_data_row:contains(TOUR TEACHER ACTIVATE) .o_list_record_selector input",
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

                // ── Flow 5 (IK text) -- "Click OK to confirm." Verified
                // against Odoo 14.0 core (list_controller.js
                // `_getActionMenuItems`): only "Archive" wraps its
                // callback in `Dialog.confirm(...)`; "Unarchive" calls
                // `_toggleArchiveState(false)` directly with no
                // confirmation dialog -- known IK inaccuracy, no dialog
                // step added here.

                // Enabling/disabling the Archived filter re-opens the
                // Filters dropdown.
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

                // ── Post-Condition — The records are restored and
                // appear again in the default list view.
                {
                    content: "Record appears again in the active list",
                    trigger: ".o_data_row:contains(TOUR TEACHER ACTIVATE)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_teacher/06-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the button opens
    // the "Select Report To Print" wizard, then closes it via Cancel. It
    // never selects a report nor clicks the wizard's own Print button,
    // because the resulting report action is an ir.actions.act_url
    // download with no DOM "finished" signal -- clicking through it
    // could hang headless Chrome.
    tour.register(
        "ssi_school_school_teacher_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Teachers menu.
            openTeacherList(),
            [
                // ── Flow 2 — Open the record to print.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR TEACHER PRINT) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Flow 3 — Click Print in the header. The button is
                // injected by ssi_print_mixin as type="action" -- its
                // `name` attribute is a numeric action id resolved at
                // render time, so it must be targeted by its visible
                // label (selectors.md §4), not by [name=...].
                {
                    content: "Click the Print button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Print')",
                    extra_trigger: ".o_form_view",
                },

                // ── Flow 4/5 boundary — the wizard is proven open, then
                // closed. Selecting the Type/Report Template and
                // clicking the wizard's own Print button are
                // intentionally NOT executed -- see the boundary comment
                // above.
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

                // ── Post-Condition (tour boundary) — the wizard is
                // closed and the Teacher form is displayed again.
                // Whether a report is actually generated and downloaded
                // is out of tour scope.
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
});
