// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_health.school_student_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by both tours below -- corresponds to
    // Flow 1 of the base school_student IK (ssi_school): "Open the School >
    // Students menu." Re-declared here (rather than required from
    // ssi_school's own tour module) because the base tour keeps this helper
    // private to its own odoo.define closure.
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

    // Assertion block shared by both tours below -- the five history
    // widgets added by the Health tab (docs/school_student/01-create.md and
    // 02-edit.md, E1 delta of ssi_school_health). Each pair of steps proves
    // one widget from "## Additional Fields" is rendered and ready to
    // accept a line: the group separator (always has text, so it is never
    // a zero-pixel readonly box -- patterns.md §O) and the widget's own
    // "Add a line" control. Delta-only: no line is filled and no value is
    // asserted -- the Additional Post-Condition (Height/Weight/Head
    // Circumference recomputed) is a computed-value fact and belongs to
    // odoo-development-unit-test, not this tour.
    function assertHealthTabFields() {
        return [
            {
                content: "Height history is displayed",
                trigger: ".o_horizontal_separator:contains(Height)",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Heights 'Add a line' control is displayed",
                trigger:
                    ".o_field_widget[name='height_ids'] .o_field_x2many_list_row_add a",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Weight history is displayed",
                trigger: ".o_horizontal_separator:contains(Weight)",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Weights 'Add a line' control is displayed",
                trigger:
                    ".o_field_widget[name='weight_ids'] .o_field_x2many_list_row_add a",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Head Circumference history is displayed",
                trigger: ".o_horizontal_separator:contains(Head Circumference)",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Head Circumferences 'Add a line' control is displayed",
                trigger:
                    ".o_field_widget[name='head_circumference_ids'] .o_field_x2many_list_row_add a",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Allergies history is displayed",
                trigger: ".o_horizontal_separator:contains(Allergies)",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Allergies 'Add a line' control is displayed",
                trigger:
                    ".o_field_widget[name='allergy_ids'] .o_field_x2many_list_row_add a",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Disease History is displayed",
                trigger: ".o_horizontal_separator:contains(Disease History)",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Disease History 'Add a line' control is displayed",
                trigger:
                    ".o_field_widget[name='disease_history_ids'] .o_field_x2many_list_row_add a",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    }

    // IK: docs/school_student/01-create.md (E1 delta -- Additional Fields)
    tour.register(
        "ssi_school_health_school_student_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Base Flow 1 — Open the School > Students menu.
            openStudentList(),
            [
                // ── Base Flow 2 — Click the New button. (14.0: "Create")
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

                // ── Additional Fields — the create form gains a Health
                // tab. Delta-only tour: it stops after the tab and its
                // five history widgets are proven to render; it does not
                // fill any line, does not fill the base required fields,
                // and does not continue to Save (see the boundary comment
                // above assertHealthTabFields).
                {
                    content: "Open the Health tab",
                    trigger: ".o_notebook .nav-link:contains(Health)",
                },
            ],
            assertHealthTabFields()
        )
    );

    // IK: docs/school_student/02-edit.md (E1 delta -- Additional Fields)
    tour.register(
        "ssi_school_health_school_student_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Base Flow 1 — Open the School > Students menu.
            openStudentList(),
            [
                // ── Base Flow 2 — Find and open the record to edit.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR STUDENT HEALTH EDIT) .o_data_cell:first",
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

                // ── Additional Fields — the Health tab described in
                // 01-create remains available for editing. Delta-only
                // tour: it stops after the tab and its five history
                // widgets are proven to still render and accept a line on
                // an existing record; it does not add/edit/remove a line,
                // and does not continue to the base Flow's Generate
                // Code/Save/Reset code steps.
                {
                    content: "Open the Health tab",
                    trigger: ".o_notebook .nav-link:contains(Health)",
                },
            ],
            assertHealthTabFields()
        )
    );
});
