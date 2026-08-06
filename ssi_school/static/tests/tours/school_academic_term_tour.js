// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school.school_academic_term_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- corresponds to
    // Flow 1 of every school_academic_term IK: "Open the School >
    // Configuration > Period > Academic Terms menu."
    // Note: "Configuration" (menu_school_configuration) is a level-2
    // section WITH children, so it renders as a clickable
    // data-menu-xmlid dropdown-toggle. "Period" (menu_period_configuration)
    // is a level-3+ menuitem with NO action= attribute and children of its
    // own, so Odoo 14.0 renders it as a plain, non-clickable
    // "<div class='dropdown-header'>" -- NOT a data-menu-xmlid link.
    // "Academic Terms" is a direct clickable leaf entry flattened into
    // that SAME Configuration dropdown, grouped visually under the
    // "Period" heading -- there is therefore no separate "click Period"
    // step (patterns.md skill odoo-development-ui-test §A).
    function openTermList() {
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
                content: "Open the Academic Terms menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.school_academic_term_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN (nama Action
                // "school_academic_term_action" = "Academic Terms") benar-
                // benar terpasang -- bukan sekadar "ada list di layar"
                // (patterns.md §A).
                content: "Academic Terms list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Academic Terms)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/school_academic_term/01-create.md
    tour.register(
        "ssi_school_school_academic_term_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Period >
            // Academic Terms menu.
            openTermList(),
            [
                // ── Flow 2 — Click the New button. (14.0: "Create")
                {
                    content: "Click Create",
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

                // ── Flow 3 — Fill in the required fields: Name, Code,
                // Academic Year, Date Start, Date End. Code is left as "/"
                // so Generate Code below (Flow 4) has something to do.
                {
                    content: "Fill in the Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR SAT Create",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },
                {
                    content: "Select the Academic Year",
                    trigger: ".o_field_many2one[name='year_id'] input",
                    run: "text TOUR SAT Academic Year",
                },
                {
                    content: "Pick the Academic Year from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR SAT Academic Year)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Date Start",
                    trigger: ".o_field_widget[name='date_start'] input",
                    run: "text 01/15/2026",
                },
                {
                    content: "Fill in the Date End",
                    trigger: ".o_field_widget[name='date_end'] input",
                    run: "text 06/15/2026",
                },

                // ── Flow 4 — Click Generate Code in the header to
                // automatically assign a code from the sequence.template
                // configured for school_academic_term.
                {
                    content: "Click Generate Code",
                    trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                },
                {
                    // Gerbang: action_generate_code auto-save + tulis +
                    // muat ulang record secara asinkron. Tombol Generate
                    // Code sendiri di-disable sinkron saat diklik
                    // (form_renderer.js disableButtons()) dan baru
                    // di-enable lagi setelah siklus auto-save +
                    // call_button + reload selesai (enableButtons()) --
                    // itulah yang ditunggu di sini (patterns.md §P).
                    content: "Generate Code call has completed",
                    trigger:
                        ".o_statusbar_buttons button[name='action_generate_code']:enabled",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 5 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — a new record is created in Unstarted
                // status, with Enrollment State set to Close. First Term /
                // Last Term are computed automatically -- both are value
                // checks, out of tour scope (odoo-development-ui-test §2).
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_academic_term/02-edit.md
    tour.register(
        "ssi_school_school_academic_term_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Period >
            // Academic Terms menu.
            openTermList(),
            [
                // ── Flow 2 — Find and open the record to edit.
                {
                    content: "Open the record",
                    trigger: ".o_data_row:contains(TOUR SAT Edit) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                // 14.0: an existing record opens read-only -- Edit first.
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

                // ── Flow 3 — Change the required fields.
                {
                    content: "Change the Name",
                    trigger: ".o_field_widget[name='name']",
                    run: "text TOUR SAT Edit Changed",
                },

                // ── Flow 4 — Code still shows "/" (set by setUpClass) --
                // click Generate Code in the header to assign a new code.
                {
                    content: "Click Generate Code",
                    trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                },
                {
                    // Gerbang -- lihat catatan gerbang di tour create di atas.
                    content: "Generate Code call has completed",
                    trigger:
                        ".o_statusbar_buttons button[name='action_generate_code']:enabled",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 5 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — the record is updated with the new
                // values. First Term / Last Term recompute is a value
                // check, out of tour scope.
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_academic_term/03-delete.md
    tour.register(
        "ssi_school_school_academic_term_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Period >
            // Academic Terms menu.
            openTermList(),
            [
                // ── Flow 2 — Select one or more records to delete (check
                // the checkbox).
                {
                    content: "Select the record to delete",
                    trigger:
                        ".o_data_row:contains(TOUR SAT Delete) .o_list_record_selector input",
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
                    content: "Record no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR SAT Delete)))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_academic_term/04-deactivate.md
    tour.register(
        "ssi_school_school_academic_term_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Period >
            // Academic Terms menu.
            openTermList(),
            [
                // ── Flow 2 — Select one or more records to deactivate
                // (check the checkbox).
                {
                    content: "Select the record to deactivate",
                    trigger:
                        ".o_data_row:contains(TOUR SAT Deactivate) .o_list_record_selector input",
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

                // ── Post-Condition — the records are archived and no
                // longer appear in the default list view. (Their
                // unavailability in new transactions, and that existing
                // transactions using them are unaffected, are not
                // kasatmata UI facts here -- out of tour scope.)
                {
                    content: "Record no longer appears in the active list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR SAT Deactivate)))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_academic_term/05-activate.md
    tour.register(
        "ssi_school_school_academic_term_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Period >
            // Academic Terms menu.
            openTermList(),
            [
                // ── Flow 2 — Enable the Archived filter in the search bar.
                {
                    content: "Open the Filters menu",
                    trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                    // 14.0: the Filters dropdown is an Owl component that
                    // does not always open on a synthetic click -- use a
                    // real browser click (patterns.md §I/§J).
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

                // ── Flow 3 — Select one or more records to reactivate
                // (check the checkbox).
                {
                    content: "Select the record to reactivate",
                    trigger:
                        ".o_data_row:contains(TOUR SAT Activate) .o_list_record_selector input",
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

                // ── Flow 5 (IK text) — "Click OK to confirm." Verified
                // against Odoo 14.0 core
                // (web/static/src/js/views/list/list_controller.js
                // _getActionMenuItems): only the "Archive" action wraps
                // its callback in Dialog.confirm(...); "Unarchive" calls
                // _toggleArchiveState(false) directly with NO confirmation
                // dialog. There is therefore no dialog step to add here --
                // this is a known inaccuracy in the IK text (same pattern
                // already documented in ssi_customer_invoice's
                // customer_invoice_type_tour.js and
                // ssi_customer_invoice_export's
                // customer_invoice_export_type_tour.js), out of scope for
                // this tour-only change.
                //
                // Gerbang wajib (patterns.md §P): tanpa ini, langkah
                // berikutnya (buka Filters lalu matikan facet Archived)
                // berlomba dengan RPC action_unarchive yang masih
                // berjalan -- terbukti di CI (race < 25ms, penyebab
                // tour ini gagal: "Confirm the dialog" langkah lama
                // sudah dibuang, tapi tanpa gerbang penggantinya
                // langkah berikutnya bisa mendahului RPC). Baris masih
                // tampil di list ter-filter Archived sebelum tombol
                // diklik, jadi begitu unarchive mendarat & list
                // reload, baris ini PASTI hilang dari situ -- gerbang
                // yang sah.
                {
                    content: "Unarchive completes (row leaves the Archived list)",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR SAT Activate)))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Enabling/disabling the Archived filter re-opens the
                // Filters dropdown -- selecting "Unarchive" above closed
                // it (any click outside the dropdown closes it; see
                // web.DropdownMenu _onWindowClick).
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

                // ── Post-Condition — the records are restored and appear
                // again in the default list view.
                {
                    content: "Record appears again in the active list",
                    trigger: ".o_data_row:contains(TOUR SAT Activate)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_academic_term/06-start.md
    tour.register(
        "ssi_school_school_academic_term_start",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Period >
            // Academic Terms menu.
            openTermList(),
            [
                // ── Flow 2 — Open the record to start.
                {
                    content: "Open the record",
                    trigger: ".o_data_row:contains(TOUR SAT Start) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 3 — Click the Start button.
                {
                    content: "Click the Start button",
                    trigger: ".o_statusbar_buttons button[name='action_open']",
                    extra_trigger: ".o_form_view",
                },

                // ── Post-Condition — Status changes to On progress: the
                // Start button (only shown while draft) is no longer
                // shown, and the Done button (only shown while open)
                // becomes available. Reading the state field value itself
                // is unit test territory (odoo-development-ui-test §2).
                {
                    content: "The Start button is no longer shown",
                    trigger:
                        ".o_statusbar_buttons:not(:has(button[name='action_open']:visible))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The Done button becomes available",
                    trigger: ".o_statusbar_buttons button[name='action_done']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_academic_term/07-finish.md
    tour.register(
        "ssi_school_school_academic_term_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Period >
            // Academic Terms menu.
            openTermList(),
            [
                // ── Flow 2 — Open the record to finish.
                {
                    content: "Open the record",
                    trigger: ".o_data_row:contains(TOUR SAT Finish) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 3 — Click the Done button (action_done).
                {
                    content: "Click the Done button",
                    trigger: ".o_statusbar_buttons button[name='action_done']",
                    extra_trigger: ".o_form_view",
                },

                // ── Post-Condition — Status changes to Done: the Done
                // button (only shown while open) is no longer shown.
                {
                    content: "The Done button is no longer shown",
                    trigger:
                        ".o_statusbar_buttons:not(:has(button[name='action_done']:visible))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_academic_term/08-restart.md
    tour.register(
        "ssi_school_school_academic_term_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Period >
            // Academic Terms menu.
            openTermList(),
            [
                // ── Flow 2 — Open the record to restart.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR SAT Restart) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 3 — Click the Restart button (action_restart).
                {
                    content: "Click the Restart button",
                    trigger: ".o_statusbar_buttons button[name='action_restart']",
                    extra_trigger: ".o_form_view",
                },

                // ── Post-Condition — Status returns to Unstarted: the
                // Restart button (hidden while draft) is no longer shown,
                // and the Start button (only shown while draft) becomes
                // available again.
                {
                    content: "The Restart button is no longer shown",
                    trigger:
                        ".o_statusbar_buttons:not(:has(button[name='action_restart']:visible))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The Start button becomes available again",
                    trigger: ".o_statusbar_buttons button[name='action_open']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_academic_term/09-open-enrollment.md
    tour.register(
        "ssi_school_school_academic_term_open_enrollment",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Period >
            // Academic Terms menu.
            openTermList(),
            [
                // ── Flow 2 — Open the record to open for enrollment.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR SAT Open Enrollment) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 3 — Click the Open Enrollment button
                // (action_open_enrollment).
                {
                    content: "Click the Open Enrollment button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_open_enrollment']",
                    extra_trigger: ".o_form_view",
                },

                // ── Post-Condition — Enrollment State changes to Open for
                // Enrollment: the Open Enrollment button (hidden while
                // enrollment_state is open) is no longer shown, and the
                // Close Enrollment button (only shown while
                // enrollment_state is open) becomes available. Whether
                // students can now be enrolled is exercised by the
                // school_enrollment tours, out of this tour's scope.
                {
                    content: "The Open Enrollment button is no longer shown",
                    trigger:
                        ".o_statusbar_buttons:not(:has(button[name='action_open_enrollment']:visible))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The Close Enrollment button becomes available",
                    trigger:
                        ".o_statusbar_buttons button[name='action_close_enrollment']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_academic_term/10-close-enrollment.md
    tour.register(
        "ssi_school_school_academic_term_close_enrollment",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Period >
            // Academic Terms menu.
            openTermList(),
            [
                // ── Flow 2 — Open the record to close for enrollment.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR SAT Close Enrollment) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 3 — Click the Close Enrollment button
                // (action_close_enrollment).
                {
                    content: "Click the Close Enrollment button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_close_enrollment']",
                    extra_trigger: ".o_form_view",
                },

                // ── Post-Condition — Enrollment State changes to Close:
                // the Close Enrollment button (hidden while
                // enrollment_state is close) is no longer shown, and the
                // Open Enrollment button (only shown while
                // enrollment_state is close) becomes available again.
                // Whether new Enrollment records can no longer be opened
                // is exercised by the school_enrollment tours, out of
                // this tour's scope.
                {
                    content: "The Close Enrollment button is no longer shown",
                    trigger:
                        ".o_statusbar_buttons:not(:has(button[name='action_close_enrollment']:visible))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The Open Enrollment button becomes available",
                    trigger:
                        ".o_statusbar_buttons button[name='action_open_enrollment']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_academic_term/11-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the button opens
    // the "Select Report To Print" wizard, then closes it via Cancel. It
    // never selects a report nor clicks the wizard's own Print button,
    // because the resulting report action is an ir.actions.act_url
    // download with no DOM "finished" signal -- clicking through it could
    // hang headless Chrome.
    tour.register(
        "ssi_school_school_academic_term_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Period >
            // Academic Terms menu.
            openTermList(),
            [
                // ── Flow 2 — Open the record to print.
                {
                    content: "Open the record",
                    trigger: ".o_data_row:contains(TOUR SAT Print) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 3 — Click Print in the header.
                // The button is injected by mixin.print_document (via
                // mixin.master_data) as type="action" -- its "name"
                // attribute is a numeric action id resolved at render
                // time, so it must be targeted by its visible label
                // (selectors.md §4), not by [name=...].
                {
                    content: "Click the Print button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Print')",
                    extra_trigger: ".o_form_view",
                },

                // ── Flow 4/5 boundary — the wizard is proven open, then
                // closed. Selecting the Type / Report Template and
                // clicking the wizard's own Print button are intentionally
                // NOT executed -- see the tour comment above.
                //
                // 14.0: do NOT prefix the trigger with ".modal" -- when a
                // modal is displayed, web_tour scopes the search to
                // $modal_displayed.find(trigger), and $modal_displayed
                // already IS the ".modal" element, so
                // ".modal .modal-title" would look for a nested modal that
                // does not exist (patterns.md §H box).
                {
                    content: "The Select Report To Print wizard is displayed",
                    trigger: ".modal-title:contains('Select Report To Print')",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Close the wizard",
                    // The button is declared with class="oe_link" in the
                    // wizard XML, but the form renderer maps it to
                    // "btn btn-link" in the DOM -- the "special" attribute
                    // survives that mapping and is the stable anchor.
                    trigger: ".modal-footer button[special='cancel']",
                    in_modal: true,
                },

                // ── Post-Condition (tour boundary) — the wizard is closed
                // and the academic term form is displayed again. Whether a
                // report is actually generated and downloaded is out of
                // tour scope.
                {
                    content: "Wizard is closed and the academic term form is displayed",
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
