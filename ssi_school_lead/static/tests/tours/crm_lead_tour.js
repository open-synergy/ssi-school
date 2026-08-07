// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_lead.crm_lead_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- Flow 1 of every crm_lead IK in this
    // module: "Open the CRM > Leads menu." "Leads" (crm.crm_menu_leads)
    // is a level-2 leaf menu carrying its own action
    // (crm.crm_lead_all_leads, name "Leads") -- it renders as a
    // clickable navbar item regardless of not being the app's landing
    // section (patterns.md §A table, row "Section (level 2)").
    function openLeadsList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the CRM app",
                trigger: '.o_app[data-menu-xmlid="crm.crm_menu_root"]',
            },
            {
                content: "Open the Leads menu",
                trigger: '.o_menu_sections [data-menu-xmlid="crm.crm_menu_leads"]',
            },
            {
                // Gerbang: opening the CRM app lands on "My Pipeline"
                // (crm_menu_sales, sequence 1) before the Leads action
                // finishes loading -- "My Pipeline" does not contain
                // "Leads" as a substring, so this gate cannot pass on the
                // stale landing view (patterns.md §A).
                content: "Leads list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Leads)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    }

    // Selects an option from an open many2one autocomplete dropdown.
    function pickMany2one(fieldName, label) {
        return [
            {
                content: "Select the " + fieldName + " field value",
                trigger: ".o_field_many2one[name='" + fieldName + "'] input",
                run: "text " + label,
            },
            {
                content: "Pick " + label + " from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(" + label + ")",
                in_modal: false,
            },
        ];
    }

    // Opens the lead record identified by its Name column value.
    function openLeadByName(leadName) {
        return [
            {
                content: "Open the lead record",
                trigger: ".o_data_row:contains(" + leadName + ") .o_data_cell:first",
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

    // IK: docs/crm_lead/01-create.md
    //
    // Delta-only tour -- this file only documents the fields this module
    // ADDS to the standard CRM Lead create form; the create flow itself
    // belongs to core CRM and has no base IK (per the file's own
    // metadata: "no base Instruksi Kerja exists for this model"). So
    // this tour only asserts the additional groups render
    // (patterns.md §O), it does not exercise any state transition.
    tour.register(
        "ssi_school_lead_crm_lead_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openLeadsList(), [
            {
                content: "Click Create",
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
            {
                content: "Prospective Student group is displayed",
                trigger: ".o_horizontal_separator:contains(Prospective Student)",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Admission Target group is displayed",
                trigger: ".o_horizontal_separator:contains(Admission Target)",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/crm_lead/02-create-admission.md
    tour.register(
        "ssi_school_lead_crm_lead_create_admission",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeadsList(),
            // Flow 2 -- Open the lead record for the prospective student.
            openLeadByName("TOUR-LEAD-ADM-001"),
            [
                // Flow 3 -- Click the Create Admission button.
                {
                    content: "Click the Create Admission button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_create_admission']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Create Admission wizard is open",
                    trigger: ".modal-title:contains(Create Admission)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ],
            // Flow 4 -- Fill in the wizard. Lead/Date/Academic Year/
            // Academic Term/School/Student are all pre-filled -- Lead by
            // the button's own context, Academic Year/Term by the
            // wizard's default_get (an open-for-admission term exists,
            // Pre-Condition setup), School/Student from the lead's own
            // fields via the button's context defaults. Only Grade has
            // no such default and must be picked here.
            pickMany2one("grade_id", "TOUR-LEAD-ADM-GRADE"),
            [
                // Flow 5 -- Click the Create button.
                {
                    content: "Click the Create button in the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },
                {
                    // Post-Condition -- the new school_admission document's
                    // form opens directly, pre-filled with this wizard's
                    // Student.
                    content: "The resulting Admission form opens",
                    trigger:
                        ".o_form_view .o_field_widget[name='student_id']:contains(TOUR-LEAD-ADM-STUDENT)",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );
});
