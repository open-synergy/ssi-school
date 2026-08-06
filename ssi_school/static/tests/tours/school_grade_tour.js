// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school.school_grade_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- Flow 1 of every
    // school_grade IK: "Open the School > Configuration > Grade > Grades
    // menu." "Grade" (ssi_school.menu_grade_configuration) is a level-3
    // grouping menuitem with no action= attribute, so 14.0 renders it as a
    // non-clickable dropdown header without data-menu-xmlid -- there is no
    // step for it (patterns.md skill odoo-development-ui-test §A).
    function openGradeList() {
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
                content: "Open the Grades menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.school_grade_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang, bukan
                // sekadar "ada list di layar" (patterns.md §A).
                content: "School Grades list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(School Grades)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/school_grade/01-create.md
    tour.register(
        "ssi_school_school_grade_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Grade > Grades
            // menu.
            openGradeList(),
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

                // ── Flow 3 — Fill in the required fields: Name, Code,
                // Type. Sequence is defaulted to 10, so it is not touched
                // here.
                {
                    content: "Fill in the Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR Grade Create",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },
                {
                    content: "Select the Type",
                    trigger: ".o_field_many2one[name='type_id'] input",
                    run: "text TOUR Grade School Grade Type",
                },
                {
                    content: "Pick the Type from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR Grade School Grade Type)",
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

                // ── Post-Condition — a new Grade record is created and
                // active.
                {
                    content: "Record is saved",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR Grade Create)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_grade/02-edit.md
    tour.register(
        "ssi_school_school_grade_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Grade > Grades
            // menu.
            openGradeList(),
            [
                // ── Flow 2 — Find and open the record to edit.
                {
                    content: "Open the record",
                    trigger: ".o_data_row:contains(TOUR Grade Edit) .o_data_cell:first",
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

                // ── Flow 3 — Change the required fields (Name, Code,
                // Type, Sequence). Only Name is changed here; Code is left
                // as "/" so Flow 4 (Generate Code) has an effect.
                {
                    content: "Change the Name",
                    trigger: ".o_field_widget[name='name']",
                    run: "text TOUR Grade Edit Changed",
                },

                // ── Flow 4 — Click Generate Code in the header to assign a
                // code from the configured sequence.template, since the
                // Code field is still "/".
                {
                    content: "Click Generate Code",
                    trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    content: "Record is saved by Generate Code",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR Grade Edit Changed)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 5 — Click Save. Changing Type or Sequence would
                // recompute Previous Grade and Next Grade for every Grade
                // of the affected Type(s); neither was changed here.
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

                // ── Flow 6 — Go back to the Grades list, select the
                // record's checkbox, click Reset code, then click OK to
                // confirm. This resets the Code field back to "/".
                {
                    content: "Click the School Grades breadcrumb to return to the list",
                    trigger: ".breadcrumb-item.o_back_button a:contains(School Grades)",
                },
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR Grade Edit Changed) .o_list_record_selector input",
                    run: "click",
                },
                {
                    content: "Click Reset code",
                    trigger: ".o_cp_buttons button[name='action_reset_code']",
                },
                {
                    // Odoo 14.0 core never reads `confirm=` on
                    // <tree><header> bulk-action buttons (only
                    // form/kanban controllers implement it -- verified:
                    // no such handling in list_controller.js or
                    // list_renderer.js). action_reset_code fires
                    // immediately with no dialog; the list then reloads
                    // and clears the row selection, which is a
                    // data-independent proof the RPC landed (the
                    // checkbox is guaranteed checked before this point).
                    content:
                        "Reset Code completes and the list reloads (row selection cleared)",
                    trigger:
                        ".o_data_row:contains(TOUR Grade Edit Changed) .o_list_record_selector input:not(:checked)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Post-Condition — the record is updated with the new
                // values.
                {
                    content: "Grades list is displayed",
                    trigger: ".o_list_view",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_grade/03-delete.md
    tour.register(
        "ssi_school_school_grade_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Grade > Grades
            // menu.
            openGradeList(),
            [
                // ── Flow 2 — Select one or more records to delete (check
                // the checkbox).
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR Grade Delete) .o_list_record_selector input",
                    run: "click",
                },

                // ── Flow 3 — Click Action > Delete.
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

                // ── Flow 4 — Click OK to confirm.
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — the selected records are permanently
                // removed from the system. Previous Grade and Next Grade of
                // the remaining Grades are automatically recomputed -- a
                // value change out of tour scope.
                //
                // `previous_grade_id`/`next_grade_id` are shown as
                // columns in this list, and their computed value can
                // display THIS record's own name inside a DIFFERENT
                // row (a still-active Grade whose "Previous"/"Next"
                // column now points elsewhere, or used to point here).
                // A bare `:has(.o_data_row:contains(...))` would match
                // that unrelated row too and could never resolve to
                // true. Scope to the char-typed Name cell specifically
                // (`.o_list_char`, exact `title=`) so the many2one
                // reference columns (`.o_list_many2one`) are excluded.
                {
                    content: "Record no longer in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_cell.o_list_char[title='TOUR Grade Delete']))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_grade/04-deactivate.md
    tour.register(
        "ssi_school_school_grade_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Grade > Grades
            // menu.
            openGradeList(),
            [
                // ── Flow 2 — Select one or more records to deactivate
                // (check the checkbox).
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR Grade Deactivate) .o_list_record_selector input",
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

                // ── Post-Condition — the records are archived and no
                // longer appear in the default list view.
                //
                // Scope to the char-typed Name cell (`.o_list_char`,
                // exact `title=`), not the whole row: `next_grade_id`/
                // `previous_grade_id` are shown as many2one columns in
                // this list and can display this record's own name
                // inside an unrelated row, which a bare
                // `:has(.o_data_row:contains(...))` would also match
                // and could never resolve to true.
                {
                    content: "Record no longer in the default list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_cell.o_list_char[title='TOUR Grade Deactivate']))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_grade/05-activate.md
    tour.register(
        "ssi_school_school_grade_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Grade > Grades
            // menu.
            openGradeList(),
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

                // ── Flow 3 — Select one or more records to reactivate
                // (check the checkbox).
                {
                    content: "Select the archived record's checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR Grade Activate) .o_list_record_selector input",
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
                // Odoo 14.0 core wraps ONLY "Archive" in Dialog.confirm
                // (list_controller.js _getActionMenuItems); "Unarchive"
                // calls _toggleArchiveState(false) directly with no
                // dialog at all -- verified via CI RPC log:
                // action_unarchive fires immediately after the click,
                // modal_displayed stays 0. There is therefore no OK
                // step to click here; the IK's Flow 5 does not apply to
                // this specific action in this Odoo series.
                //
                // Gerbang wajib (patterns.md §P): tanpa ini, langkah
                // berikutnya (buka Filters lalu matikan facet Archived)
                // berlomba dengan RPC action_unarchive yang masih
                // berjalan -- terbukti di CI (race < 25ms). Baris masih
                // tampil di list ter-filter Archived sebelum tombol
                // diklik, jadi begitu unarchive mendarat & list reload,
                // baris ini PASTI hilang dari situ -- gerbang yang sah.
                // Scope ke sel Name char-typed (bukan seluruh baris):
                // next_grade_id/previous_grade_id adalah kolom many2one
                // yang bisa menampilkan nama record ini di BARIS LAIN,
                // dan `:has(.o_data_row:contains(...))` polos bisa
                // salah cocok ke situ.
                {
                    content: "Unarchive completes (row leaves the Archived list)",
                    trigger:
                        ".o_list_view:not(:has(.o_data_cell.o_list_char[title='TOUR Grade Activate']))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Post-Condition — the records are restored and appear
                // again in the default list view. Remove the Archived
                // filter facet to observe the default list.
                {
                    content: "Remove the Archived filter",
                    trigger: ".o_searchview_facet .o_facet_remove",
                    run: "click",
                },
                {
                    content: "Record appears again in the default list",
                    trigger: ".o_data_row:contains(TOUR Grade Activate)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_grade/06-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the button opens the
    // "Select Report To Print" wizard, then closes it via Cancel. It never
    // selects a report nor clicks the wizard's own Print button, because
    // the resulting report action is an ir.actions.act_url download with
    // no DOM "finished" signal -- clicking through it could hang headless
    // Chrome.
    tour.register(
        "ssi_school_school_grade_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Grade > Grades
            // menu.
            openGradeList(),
            [
                // ── Flow 2 — Open the record to print.
                {
                    content: "Open the grade record",
                    trigger:
                        ".o_data_row:contains(TOUR PRINT GRADE) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Grade form is displayed",
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
                // closed. Selecting the report and clicking the wizard's
                // own Print button are intentionally NOT executed -- see
                // the module docstring above.
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
                // and the grade form is displayed again. Whether a report
                // is actually generated and downloaded is out of tour
                // scope.
                {
                    content: "Wizard is closed and the grade form is displayed",
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
