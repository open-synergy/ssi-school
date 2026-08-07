// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_admission_lead.crm_lead_tour", function (require) {
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
    // metadata: "no base Instruksi Kerja exists for this model"). The
    // fields added here are plain (non-related, non-readonly) widgets,
    // so they render with a visible box even while empty -- anchor
    // directly to the widgets, unlike the readonly-empty case in
    // patterns.md §O.
    tour.register(
        "ssi_school_admission_lead_crm_lead_create",
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
                content: "Grade field is displayed",
                trigger: ".o_field_widget[name='grade_id']",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Previous School field is displayed",
                trigger: ".o_field_widget[name='previous_school_id']",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/crm_lead/02-create-admission-form.md
    tour.register(
        "ssi_school_admission_lead_crm_lead_create_admission_form",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeadsList(),
            // Flow 2 -- Open the lead record for the prospective student.
            openLeadByName("TOUR-LEAD-ADF-001"),
            [
                // Flow 3 -- Click the Create Admission Form button.
                {
                    content: "Click the Create Admission Form button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_create_admission_form']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Create Admission Form wizard is open",
                    trigger: ".modal-title:contains(Create Admission Form)",
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
            // fields via the button's context defaults. Pricelist,
            // Grade, and Parent have no such default (Grade explicitly
            // NOT pre-filled from the lead's own Grade field per the IK)
            // and must be picked here. Fee Template is documented as
            // "Optional", but action_confirm() only sets the resulting
            // school_admission_form's required journal_id/account_id
            // when one is selected -- picking it here follows the only
            // path that actually completes the Flow.
            pickMany2one("pricelist_id", "TOUR-LEAD-ADF-PRICELIST"),
            pickMany2one("grade_id", "TOUR-LEAD-ADF-GRADE"),
            pickMany2one("fee_template_id", "TOUR-LEAD-ADF-FEE-TEMPLATE"),
            pickMany2one("parent_id", "TOUR-LEAD-ADF-PARENT"),
            [
                // Flow 5 -- Click the Create button.
                {
                    content: "Click the Create button in the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },
                {
                    // Post-Condition -- the new school_admission_form
                    // document's form opens directly, pre-filled with
                    // this wizard's Student.
                    content: "The resulting Admission Form opens",
                    trigger:
                        ".o_form_view .o_field_widget[name='student_id']:contains(TOUR-LEAD-ADF-STUDENT)",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/crm_lead/03-open-admission-test.md
    tour.register(
        "ssi_school_admission_lead_crm_lead_open_admission_test",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeadsList(),
            // Flow 2 -- Open the lead record whose Admission Test field
            // is set.
            openLeadByName("TOUR-LEAD-OAT-001"),
            [
                // Flow 3 -- Click the Admission Test button.
                {
                    content: "Click the Admission Test button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_open_admission_test']",
                    extra_trigger: ".o_form_view",
                },
                {
                    // Post-Condition -- the linked school_admission_test
                    // document's form opens, replacing the lead's own
                    // form view.
                    content: "The linked Admission Test form opens",
                    trigger:
                        ".o_form_view .o_field_widget[name='student_id']:contains(TOUR-LEAD-OAT-STUDENT)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );
});
