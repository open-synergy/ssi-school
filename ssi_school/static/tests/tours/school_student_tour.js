// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school.school_student_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- corresponds
    // to Flow 1 of every school_student IK: "Open the School > Students
    // menu." "Students" is a direct child of the School app root
    // (menu_school_root) with no children of its own, so it renders as
    // a single clickable navbar entry -- there is no Configuration step
    // in between.
    function openStudentList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the School app",
                trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
            },
            {
                content: "Open the Students menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.school_student_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang,
                // bukan sekadar "ada list di layar" (patterns.md §A).
                content: "Students list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Students)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/school_student/01-create.md
    tour.register(
        "ssi_school_school_student_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Students menu.
            openStudentList(),
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
                // Contact.
                {
                    content: "Fill in the Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR STUDENT CREATE",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },
                {
                    content: "Select the Contact",
                    trigger: ".o_field_many2one[name='contact_id'] input",
                    run: "text TOUR STUDENT CONTACT CREATE",
                },
                {
                    content: "Pick the Contact from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR STUDENT CONTACT CREATE)",
                    in_modal: false,
                },

                // ── Flow 4 — On the Personal Information tab, review or
                // fill in the identity, birth place, health, and
                // socio-cultural fields synchronized from the contact
                // (optional -- none of these fields are required to
                // save, so only the tab render is verified).
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

                // ── Flow 6 — On the Enrollment tab, select the required
                // School. Initial Grade Type is automatically filled
                // from School (read-only) and Initial Grade is optional
                // -- neither is exercised here.
                {
                    content: "Open the Enrollments tab",
                    trigger: ".o_notebook .nav-link:contains(Enrollments)",
                },
                {
                    content: "Select the School",
                    trigger: ".o_field_many2one[name='school_id'] input",
                    run: "text TOUR STUDENT SCHOOL",
                },
                {
                    content: "Pick the School from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR STUDENT SCHOOL)",
                    in_modal: false,
                },

                // ── Flow 7 — On the Family tab, review or fill in
                // Father, Mother, and Guardian as needed (optional --
                // only the tab render is verified).
                {
                    content: "Open the Family tab",
                    trigger: ".o_notebook .nav-link:contains(Family)",
                },
                {
                    content: "Family tab is displayed",
                    trigger: ".o_field_widget[name='father_id']",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Flow 8 — On the Bank Accounts tab, add lines as
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

                // ── Flow 9 — Click Generate Code in the header.
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

                // ── Flow 10 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — A new Student record is created in
                // the Waiting for Enrollment status. (Current Grade,
                // Next Grade, Active Enrollment, and Grade Class are
                // computed values -- out of tour scope, see
                // odoo-development-unit-test.)
                {
                    content: "Student record is saved and displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR STUDENT CREATE)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    // Web.FieldBadge (Owl) renders a single <span
                    // class="badge badge-pill o_field_badge
                    // o_field_widget" name="state">...</span> -- there
                    // is no wrapping div, so `o_field_widget` and
                    // `o_field_badge` are classes on the SAME element,
                    // not ancestor/descendant. Verified against the
                    // actual CI DOM dump and against
                    // web/static/src/xml/fields.xml `t-name="web.
                    // FieldBadge"` + web.AbstractFieldOwl (which adds
                    // o_field_widget to the component's own root).
                    content: "Status badge shows Waiting for Enrollment",
                    trigger:
                        ".o_field_widget.o_field_badge[name='state']:contains(Waiting for Enrollment)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_student/02-edit.md
    tour.register(
        "ssi_school_school_student_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Students menu.
            openStudentList(),
            [
                // ── Flow 2 — Find and open the record to edit.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR STUDENT EDIT) .o_data_cell:first",
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

                // ── Flow 3 — Change the required fields. (Changing
                // Contact/School would re-synchronize other tabs -- not
                // exercised here, only Name is changed as the
                // representative required field.)
                {
                    content: "Change the Name",
                    trigger: ".o_field_widget[name='name']",
                    run: "text TOUR STUDENT EDIT CHANGED",
                },

                // ── Flow 4 — Update Personal Information, Contact &
                // Address, Family, Initial Grade, or Bank Accounts
                // fields as needed (optional -- not exercised here, see
                // the create tour above for the tab-render coverage).

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
                // Code again: go back to the Students list, select the
                // record's checkbox, click Reset code in the header,
                // then click OK to confirm.
                {
                    content: "Click the Students breadcrumb",
                    trigger: ".breadcrumb-item.o_back_button a:contains(Students)",
                },
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR STUDENT EDIT CHANGED) .o_list_record_selector input",
                    run: "click",
                },
                {
                    content: "Click Reset code in the list toolbar",
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
                        ".o_data_row:contains(TOUR STUDENT EDIT CHANGED) .o_list_record_selector input:not(:checked)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Post-Condition — The record is updated with the
                // new values.
                {
                    content: "Students list is displayed",
                    trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_student/03-delete.md
    tour.register(
        "ssi_school_school_student_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Students menu.
            openStudentList(),
            [
                // ── Flow 2 — Select one or more records to delete
                // (check the checkbox).
                {
                    content: "Select the record to delete",
                    trigger:
                        ".o_data_row:contains(TOUR STUDENT DELETE) .o_list_record_selector input",
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
                // res.partner contact record itself is not deleted (not
                // a kasatmata UI fact here -- out of tour scope).
                {
                    content: "Record no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR STUDENT DELETE)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_student/04-deactivate.md
    tour.register(
        "ssi_school_school_student_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Students menu.
            openStudentList(),
            [
                // ── Flow 2 — Select one or more records to deactivate
                // (check the checkbox).
                {
                    content: "Select the record to deactivate",
                    trigger:
                        ".o_data_row:contains(TOUR STUDENT DEACTIVATE) .o_list_record_selector input",
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
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR STUDENT DEACTIVATE)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_student/05-activate.md
    tour.register(
        "ssi_school_school_student_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Students menu.
            openStudentList(),
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
                        ".o_data_row:contains(TOUR STUDENT ACTIVATE) .o_list_record_selector input",
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
                //
                // Gerbang wajib (patterns.md §P): tanpa ini, langkah
                // berikutnya (buka Filters lalu matikan facet Archived)
                // berlomba dengan RPC action_unarchive yang masih
                // berjalan -- terbukti di CI (race < 25ms pada tour
                // school_academic_term_activate yang berbagi pola ini).
                // Baris masih tampil di list ter-filter Archived
                // sebelum tombol diklik, jadi begitu unarchive
                // mendarat & list reload, baris ini PASTI hilang dari
                // situ -- gerbang yang sah.
                {
                    content: "Unarchive completes (row leaves the Archived list)",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR STUDENT ACTIVATE)))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

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
                    trigger: ".o_data_row:contains(TOUR STUDENT ACTIVATE)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_student/06-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the button opens
    // the "Select Report To Print" wizard, then closes it via Cancel. It
    // never selects a report nor clicks the wizard's own Print button,
    // because the resulting report action is an ir.actions.act_url
    // download with no DOM "finished" signal -- clicking through it
    // could hang headless Chrome.
    tour.register(
        "ssi_school_school_student_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Students menu.
            openStudentList(),
            [
                // ── Flow 2 — Open the record to print.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR STUDENT PRINT) .o_data_cell:first",
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
                // closed and the Student form is displayed again.
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
