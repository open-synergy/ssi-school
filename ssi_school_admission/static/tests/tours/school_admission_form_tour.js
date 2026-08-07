// Copyright 2022 OpenSynergy Indonesia
// Copyright 2022 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_admission.school_admission_form_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- corresponds to Flow 1 of every
    // school_admission_form IK: "Open the School > Admission > Forms
    // menu." "Admission" (menu_school_admission) is a level-2 section
    // WITH children -> renders as a clickable dropdown-toggle regardless
    // of it having no action= of its own (patterns.md §A table, row
    // "Section (level 2)").
    function openFormList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the School app",
                trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
            },
            {
                content: "Open the Admission menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_admission.menu_school_admission"]',
            },
            {
                content: "Open the Forms menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_admission.school_admission_form_menu"]',
            },
            {
                content: "Forms list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Forms)",
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

    // Opens the record identified by its Student column value.
    function openRecordByStudent(studentName) {
        return [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(" + studentName + ") .o_data_cell:first",
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

    // Clicks a header button whose rendered `name` is a numeric action id
    // (type="action"), matched by its EXACT visible label so it is not
    // confused with a similarly-worded sibling button (selectors.md §4;
    // patterns.md §I -- exact match, not :contains substring).
    function clickButtonByExactLabel(label) {
        return {
            content: "Click the " + label + " button",
            trigger: ".o_form_view button:enabled",
            run: function () {
                var $btn = $(".o_form_view button:enabled").filter(function () {
                    return $(this).text().trim() === label;
                });
                $btn[0].click();
            },
        };
    }

    // IK: docs/school_admission_form/01-create.md
    tour.register(
        "ssi_school_admission_school_admission_form_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            [
                // Flow 2 -- Click New. (14.0: "Create")
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
            ],
            // Flow 3 -- Fill in the required fields.
            pickMany2one("academic_year_id", "TOUR ADM FORM Academic Year"),
            pickMany2one("academic_term_id", "TOUR ADM FORM Term"),
            pickMany2one("student_id", "TOUR ADM FORM Create Student"),
            pickMany2one("parent_id", "TOUR ADM FORM Parent"),
            pickMany2one("school_id", "TOUR ADM FORM School"),
            pickMany2one("grade_id", "TOUR ADM FORM Grade"),
            pickMany2one("pricelist_id", "TOUR ADM FORM Pricelist"),
            [
                // Flow 4 -- On the Fee Details tab, select a Fee
                // Template.
                {
                    content: "Open the Fee Details tab",
                    trigger: ".o_notebook .nav-link:contains(Fee Details)",
                },
            ],
            pickMany2one("fee_template_id", "TOUR ADM FORM Fee Template"),
            [
                // Flow 5 -- Click Compute Fee.
                {
                    content: "Click Compute Fee",
                    trigger: ".o_form_view button[name='action_compute_fee']",
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Fee lines are computed from the template",
                    trigger:
                        ".o_field_x2many[name='line_ids'] .o_data_row:contains(TOUR ADM FORM Fee Line)",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 6 -- On the Accounting tab, click Compute Tax.
                {
                    content: "Open the Accounting tab",
                    trigger: ".o_notebook .nav-link:contains(Accounting)",
                },
                {
                    content: "Click Compute Tax",
                    trigger: ".o_form_view button[name='action_compute_tax']",
                },

                // Flow 7 -- Click Save.
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
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission_form/02-edit.md
    tour.register(
        "ssi_school_admission_school_admission_form_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Edit Student"),
            [
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
            ],
            // Flow 3 -- Change one required field.
            pickMany2one("grade_id", "TOUR ADM FORM Grade"),
            [
                // Flow 4 -- Compute Fee refreshes the fee lines.
                {
                    content: "Open the Fee Details tab",
                    trigger: ".o_notebook .nav-link:contains(Fee Details)",
                },
                {
                    content: "Click Compute Fee",
                    trigger: ".o_form_view button[name='action_compute_fee']",
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Fee lines are refreshed from the template",
                    trigger:
                        ".o_field_x2many[name='line_ids'] .o_data_row:contains(TOUR ADM FORM Fee Line)",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 5 -- Compute Tax.
                {
                    content: "Open the Accounting tab",
                    trigger: ".o_notebook .nav-link:contains(Accounting)",
                },
                {
                    content: "Click Compute Tax",
                    trigger: ".o_form_view button[name='action_compute_tax']",
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
            ]
        )
    );

    // IK: docs/school_admission_form/03-delete.md
    tour.register(
        "ssi_school_admission_school_admission_form_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Delete Student"),
            [
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
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Click the Forms breadcrumb",
                    trigger: ".breadcrumb-item.o_back_button a:contains(Forms)",
                },
                {
                    content: "Record no longer in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR ADM FORM Delete Student)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission_form/04-confirm.md
    tour.register(
        "ssi_school_admission_school_admission_form_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Confirm Student"),
            [
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Status is Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission_form/05-approve.md
    tour.register(
        "ssi_school_admission_school_admission_form_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Approve Student"),
            [
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                // This fixture is a FREE form (no fee lines), so
                // _20_auto_done_if_free fires as part of the same
                // approval call and the record lands directly on Done
                // (05-approve.md note; see 09-finish.md).
                {
                    content: "Status is Done",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission_form/06-reject.md
    tour.register(
        "ssi_school_admission_school_admission_form_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Reject Student"),
            [
                {
                    content: "Click the Reject button",
                    trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Status is Rejected",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // NOTE: 09-finish.md has no manual step (its transition is fired by
    // a base.automation rule reacting to Journal Item reconciliation,
    // not a button) -- scope-and-boundaries.md §1 rule 6: no UI step ->
    // no tour, unit test only.

    // IK: docs/school_admission_form/10-cancel.md
    tour.register(
        "ssi_school_admission_school_admission_form_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Cancel Student"),
            [
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                    extra_trigger: ".o_form_view",
                },
                {
                    // 14.0: JANGAN prefiks `.modal` (patterns.md §H).
                    content: "Wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Select the cancellation reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] " +
                        ".o_radio_item:contains(TOUR ADM FORM Cancel Reason) input",
                    run: "click",
                },
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },
                {
                    content: "Confirm the Are you sure? dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Status is Cancelled",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission_form/12-restart.md
    tour.register(
        "ssi_school_admission_school_admission_form_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Restart Student"),
            [
                {
                    content: "Click the Restart button",
                    trigger: ".o_statusbar_buttons button[name='action_restart']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission_form/13-reset-number.md
    tour.register(
        "ssi_school_admission_school_admission_form_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Reset Number Student"),
            [
                {
                    content: "Click the Reset Document Number button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reset_document_number']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    // After the reset, the form re-renders read-only, so
                    // the visible field is display_name; name_get()
                    // renders "/" as "*<id>".
                    content: "Document number is reset (display name shows *)",
                    trigger:
                        ".oe_title .o_field_widget[name='display_name']:contains(*)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission_form/14-restart-approval.md
    tour.register(
        "ssi_school_admission_school_admission_form_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Restart Approval Student"),
            [
                {
                    content: "Click the Restart Approval Process button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reload_approval_template']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Status remains Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission_form/15-create-admission.md
    //
    // Boundary (Design Decision of ssi-school#227): only verifies the
    // resulting document opens; the wizard's own field values are not
    // asserted (unit test territory).
    tour.register(
        "ssi_school_admission_school_admission_form_create_admission",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Create Admission Student"),
            [
                clickButtonByExactLabel("Create Admission"),
                {
                    content: "Create School Admission wizard is open",
                    trigger: ".modal-title:contains('Create School Admission')",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Click Create Admission in the wizard",
                    trigger: ".modal-footer button[name='action_create_admission']",
                },
                {
                    // Post-Condition -- the resulting school_admission
                    // form opens directly.
                    content: "The resulting School Admission form opens",
                    trigger:
                        ".o_form_view .o_field_widget[name='student_id']:contains(TOUR ADM FORM Create Admission Student)",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission_form/16-create-admission-test.md
    //
    // Boundary (Design Decision of ssi-school#227): only verifies the
    // resulting document opens/its notification, not its count/content.
    tour.register(
        "ssi_school_admission_school_admission_form_create_admission_test",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Create Test Student"),
            [
                {
                    content: "Click the Create Admission Test button",
                    trigger: ".o_form_view button[name='action_create_admission_test']",
                    extra_trigger: ".o_form_view",
                },
                {
                    // Post-Condition -- a new school_admission_test opens
                    // directly, pre-filled from this form.
                    content: "The resulting Admission Test form opens",
                    trigger:
                        ".o_form_view .o_field_widget[name='student_id']:contains(TOUR ADM FORM Create Test Student)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission_form/17-print.md
    tour.register(
        "ssi_school_admission_school_admission_form_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Print Student"),
            [
                {
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
            ]
        )
    );

    // IK: docs/school_admission_form/18-reload-template-policy.md
    tour.register(
        "ssi_school_admission_school_admission_form_reload_template_policy",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openFormList(),
            openRecordByStudent("TOUR ADM FORM Reload Policy Student"),
            [
                {
                    content: "Open the Policies tab",
                    trigger: ".o_notebook .nav-link:contains(Policies)",
                },
                {
                    content: "Click Reload Template Policy",
                    trigger: "button[name='action_reload_policy_template']",
                },
                {
                    content: "Policy Template is reloaded",
                    trigger:
                        ".o_field_widget[name='policy_template_id']:contains(Standard)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );
});
