// Copyright 2022 OpenSynergy Indonesia
// Copyright 2022 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_admission.school_admission_test_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- corresponds to Flow 1 of every
    // school_admission_test IK: "Open the School > Admission > Tests
    // menu."
    function openTestList() {
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
                content: "Open the Tests menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_admission.school_admission_test_menu"]',
            },
            {
                content: "Tests list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Tests)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    }

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

    // IK: docs/school_admission_test/01-create.md
    tour.register(
        "ssi_school_admission_school_admission_test_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openTestList(),
            [
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
            // Flow 3 -- Fill in the required fields. Admission Form is
            // left empty (Student is filled manually instead).
            pickMany2one("academic_year_id", "TOUR ADM TEST Academic Year"),
            pickMany2one("academic_term_id", "TOUR ADM TEST Term"),
            pickMany2one("school_id", "TOUR ADM TEST School"),
            pickMany2one("grade_id", "TOUR ADM TEST Grade"),
            pickMany2one("student_id", "TOUR ADM TEST Create Student"),
            [
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

    // IK: docs/school_admission_test/02-edit.md
    tour.register(
        "ssi_school_admission_school_admission_test_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openTestList(),
            openRecordByStudent("TOUR ADM TEST Edit Student"),
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
            pickMany2one("grade_id", "TOUR ADM TEST Grade"),
            [
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

    // IK: docs/school_admission_test/03-delete.md
    tour.register(
        "ssi_school_admission_school_admission_test_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTestList(), openRecordByStudent("TOUR ADM TEST Delete Student"), [
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
                content: "Click the Tests breadcrumb",
                trigger: ".breadcrumb-item.o_back_button a:contains(Tests)",
            },
            {
                content: "Record no longer in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR ADM TEST Delete Student)))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/school_admission_test/04-confirm.md
    tour.register(
        "ssi_school_admission_school_admission_test_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openTestList(),
            openRecordByStudent("TOUR ADM TEST Confirm Student"),
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

    // IK: docs/school_admission_test/05-approve.md
    tour.register(
        "ssi_school_admission_school_admission_test_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openTestList(),
            openRecordByStudent("TOUR ADM TEST Approve Student"),
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
                {
                    content: "Status is On Progress",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission_test/06-reject.md
    tour.register(
        "ssi_school_admission_school_admission_test_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTestList(), openRecordByStudent("TOUR ADM TEST Reject Student"), [
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
        ])
    );

    // IK: docs/school_admission_test/09-finish.md
    tour.register(
        "ssi_school_admission_school_admission_test_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTestList(), openRecordByStudent("TOUR ADM TEST Finish Student"), [
            // Flow 3 -- On the Test Result tab, check Passed.
            {
                content: "Open the Test Result tab",
                trigger: ".o_notebook .nav-link:contains(Test Result)",
            },
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
            {
                content: "Check Passed",
                trigger:
                    ".o_field_widget[name='passed'] input[type='checkbox']:not(:checked)",
                run: "click",
            },
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

            // Flow 4 -- Click the Done button.
            {
                content: "Click the Done button",
                trigger: ".o_statusbar_buttons button[name='action_done']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/school_admission_test/10-cancel.md
    tour.register(
        "ssi_school_admission_school_admission_test_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTestList(), openRecordByStudent("TOUR ADM TEST Cancel Student"), [
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                extra_trigger: ".o_form_view",
            },
            {
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
                    ".o_radio_item:contains(TOUR ADM TEST Cancel Reason) input",
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
        ])
    );

    // IK: docs/school_admission_test/12-restart.md
    tour.register(
        "ssi_school_admission_school_admission_test_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openTestList(),
            openRecordByStudent("TOUR ADM TEST Restart Student"),
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

    // IK: docs/school_admission_test/13-reset-number.md
    tour.register(
        "ssi_school_admission_school_admission_test_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openTestList(),
            openRecordByStudent("TOUR ADM TEST Reset Number Student"),
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

    // IK: docs/school_admission_test/14-restart-approval.md
    tour.register(
        "ssi_school_admission_school_admission_test_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openTestList(),
            openRecordByStudent("TOUR ADM TEST Restart Approval Student"),
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

    // IK: docs/school_admission_test/15-create-school-admission.md
    //
    // Boundary (Design Decision of ssi-school#227): only verifies the
    // resulting document opens.
    tour.register(
        "ssi_school_admission_school_admission_test_create_school_admission",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openTestList(),
            openRecordByStudent("TOUR ADM TEST Create Admission Student"),
            [
                {
                    content: "Click the Create School Admission button",
                    trigger: ".o_form_view button:enabled",
                    run: function () {
                        var $btn = $(".o_form_view button:enabled").filter(function () {
                            return $(this).text().trim() === "Create School Admission";
                        });
                        $btn[0].click();
                    },
                },
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
                    content: "The resulting School Admission form opens",
                    trigger:
                        ".o_form_view .o_field_widget[name='student_id']:contains(TOUR ADM TEST Create Admission Student)",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission_test/16-print.md
    tour.register(
        "ssi_school_admission_school_admission_test_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTestList(), openRecordByStudent("TOUR ADM TEST Print Student"), [
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
        ])
    );

    // IK: docs/school_admission_test/17-reload-template-policy.md
    tour.register(
        "ssi_school_admission_school_admission_test_reload_template_policy",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openTestList(),
            openRecordByStudent("TOUR ADM TEST Reload Policy Student"),
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
