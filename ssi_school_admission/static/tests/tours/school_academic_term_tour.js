// Copyright 2024 OpenSynergy Indonesia
// Copyright 2024 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_admission.school_academic_term_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Navigation is sourced from the BASE ssi_school IK
    // (ssi_school/docs/school_academic_term/01-create.md Flow 1), since
    // the delta IK files of this module carry no Flow of their own --
    // only "## Additional Fields" (odoo-development-ui-test
    // scope-and-boundaries.md "Backing dua-file"). "Configuration" is a
    // level-2 section WITH children -> clickable dropdown-toggle.
    // "Period" (menu_period_configuration) is a level-3+ grouping
    // menuitem with NO action -> non-clickable header, no step for it.
    // "Academic Terms" is the leaf action flattened into the same
    // Configuration dropdown.
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
                // Gerbang: tunggu action TUJUAN benar-benar terpasang
                // (patterns.md §A).
                content: "Academic Terms list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Academic Terms)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    }

    // IK: docs/school_academic_term/01-create.md (delta -- E1 archetype:
    // ## Additional Fields only, no own Flow/Post-Condition). Per
    // scope-and-boundaries.md §3 "Modul extension" table, an E1 tour is
    // delta-only: open menu -> New -> assert the new field renders ->
    // stop. It intentionally does NOT continue into Save, mirroring the
    // base create tour's own coverage of that (ssi_school's own
    // school_academic_term_tour.js already exercises the full create
    // flow for the base fields).
    tour.register(
        "ssi_school_admission_school_academic_term_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 (base IK) -- Open the Academic Terms menu.
            openTermList(),
            [
                // Flow 2 (base IK) -- Click the New button. (14.0:
                // "Create")
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

                // Delta assertion -- the Enrollment tab gains the "Open
                // for Admission" field when this module is installed.
                {
                    content: "Open the Enrollment tab",
                    trigger: ".o_notebook .nav-link:contains(Enrollment)",
                },
                {
                    content: "Open for Admission field is rendered",
                    trigger: ".o_field_widget[name='is_open_admission']",
                    run: function () {
                        // Assertion only; the delta tour stops here.
                    },
                },
            ]
        )
    );

    // IK: docs/school_academic_term/02-edit.md (delta -- same E1
    // archetype as 01-create, in the edit context). Navigation to an
    // existing record is sourced from the base IK's own 02-edit.md Flow
    // 1/2.
    tour.register(
        "ssi_school_admission_school_academic_term_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 (base IK) -- Open the Academic Terms menu.
            openTermList(),
            [
                // Flow 2 (base IK) -- Find and open the record to edit.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR ADM TERM Edit) .o_data_cell:first",
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
                // (patterns.md §E).
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

                // Delta assertion -- the Enrollment tab's "Open for
                // Admission" field is rendered and editable.
                {
                    content: "Open the Enrollment tab",
                    trigger: ".o_notebook .nav-link:contains(Enrollment)",
                },
                {
                    content: "Open for Admission field is rendered and editable",
                    trigger:
                        ".o_field_widget[name='is_open_admission'] input:enabled",
                    run: function () {
                        // Assertion only; the delta tour stops here.
                    },
                },
            ]
        )
    );
});
