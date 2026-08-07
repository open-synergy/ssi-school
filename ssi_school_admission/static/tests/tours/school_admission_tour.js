// Copyright 2024 OpenSynergy Indonesia
// Copyright 2024 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_admission.school_admission_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- corresponds to Flow 1 of every
    // school_admission IK: "Open the School > Admission > Admissions
    // menu."
    function openAdmissionList() {
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
                content: "Open the Admissions menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_admission.school_admission_menu"]',
            },
            {
                content: "Admissions list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Admissions)",
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

    // IK: docs/school_admission/01-create.md
    //
    // Flow 6's per-line Payment Term row buttons (Create/Delete/
    // Disconnect Invoice, Mark/Unmark as Manual, Duplicate Term) are
    // documented as Inline Actions but not exercised here -- same
    // convention as ssi_school's school_enrollment_tour.js.
    tour.register(
        "ssi_school_admission_school_admission_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
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
            // Flow 3 -- Fill in the required fields.
            pickMany2one("academic_year_id", "TOUR ADM Academic Year"),
            pickMany2one("academic_term_id", "TOUR ADM Term"),
            pickMany2one("school_id", "TOUR ADM School"),
            pickMany2one("grade_id", "TOUR ADM Grade"),
            pickMany2one("student_id", "TOUR ADM Create Student"),
            [
                // Flow 4 -- On the Fee tab, select a Payment Template.
                {
                    content: "Open the Fee tab",
                    trigger: ".o_notebook .nav-link:contains(Fee)",
                },
            ],
            pickMany2one("payment_template_id", "TOUR ADM Payment Template"),
            [
                // Flow 5 -- Click Compute Payment.
                {
                    content: "Click Compute Payment",
                    trigger: ".o_form_view button[name='action_compute_payment']",
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Payment Terms are computed from the template",
                    trigger:
                        ".o_field_x2many[name='payment_term_ids'] .o_data_row:contains(TOUR ADM Payment Term)",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 7 -- On the Accounting tab, fields are already
                // filled from the template (Compute Payment step above);
                // nothing left to change.

                // Flow 8 -- Click Save.
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

    // IK: docs/school_admission/02-edit.md
    tour.register(
        "ssi_school_admission_school_admission_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Edit Student"),
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
            pickMany2one("grade_id", "TOUR ADM Grade"),
            [
                {
                    content: "Open the Fee tab",
                    trigger: ".o_notebook .nav-link:contains(Fee)",
                },
                {
                    content: "Click Compute Payment",
                    trigger: ".o_form_view button[name='action_compute_payment']",
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Payment Terms are refreshed from the template",
                    trigger:
                        ".o_field_x2many[name='payment_term_ids'] .o_data_row:contains(TOUR ADM Payment Term)",
                    run: function () {
                        // Assertion only.
                    },
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
            ]
        )
    );

    // IK: docs/school_admission/03-delete.md
    tour.register(
        "ssi_school_admission_school_admission_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Delete Student"),
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
                    content: "Click the Admissions breadcrumb",
                    trigger: ".breadcrumb-item.o_back_button a:contains(Admissions)",
                },
                {
                    content: "Record no longer in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR ADM Delete Student)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission/04-confirm.md
    tour.register(
        "ssi_school_admission_school_admission_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Confirm Student"),
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

    // IK: docs/school_admission/05-approve.md
    tour.register(
        "ssi_school_admission_school_admission_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Approve Student"),
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

    // IK: docs/school_admission/06-reject.md
    tour.register(
        "ssi_school_admission_school_admission_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Reject Student"),
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

    // IK: docs/school_admission/09-finish.md
    tour.register(
        "ssi_school_admission_school_admission_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Finish Student"),
            [
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
            ]
        )
    );

    // IK: docs/school_admission/10-cancel.md
    tour.register(
        "ssi_school_admission_school_admission_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Cancel Student"),
            [
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
                        ".o_radio_item:contains(TOUR ADM Cancel Reason) input",
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

    // IK: docs/school_admission/12-restart.md
    tour.register(
        "ssi_school_admission_school_admission_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Restart Student"),
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

    // IK: docs/school_admission/13-reset-number.md
    tour.register(
        "ssi_school_admission_school_admission_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Reset Number Student"),
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

    // IK: docs/school_admission/14-restart-approval.md
    tour.register(
        "ssi_school_admission_school_admission_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Restart Approval Student"),
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

    // IK: docs/school_admission/15-create-due-invoice.md
    tour.register(
        "ssi_school_admission_school_admission_create_due_invoice",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Invoice Student"),
            [
                {
                    content: "Click the Create Due Invoice button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_open_create_due_invoice_wizard']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
                // Flow 4 -- this record is pre-selected (Admissions
                // field, readonly many2many tags). Flow 5 -- Date
                // Start/Date End left empty.
                {
                    content: "Click Create Due Invoice in the wizard",
                    trigger: ".modal-footer button[name='action_create_due_invoice']",
                },
                {
                    content: "Wizard is closed",
                    trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Open the Fee tab",
                    trigger: ".o_notebook .nav-link:contains(Fee)",
                },
                {
                    // [name='state'] never matches: 14.0's list_renderer.js
                    // only sets a class on <td>, never a name attribute
                    // (verified against source) -- scope to the row that
                    // has the term's own exact Name cell, then look for
                    // "Invoiced" anywhere in that same row.
                    content: "Payment term status is now Invoiced",
                    trigger:
                        ".o_data_row:has(.o_data_cell.o_list_char[title='TOUR ADM DUE TERM']) .o_data_cell:contains(Invoiced)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission/16-create-enrollment.md
    //
    // Boundary (Design Decision of ssi-school#227): only verifies the
    // resulting document opens; wizard field values are unit test
    // territory.
    tour.register(
        "ssi_school_admission_school_admission_create_enrollment",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Enrollment Student"),
            [
                {
                    content: "Click the Create Enrollment button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_create_enrollment']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Create Enrollment wizard is open",
                    trigger: ".modal-title:contains('Create Enrollment')",
                    run: function () {
                        // Assertion only.
                    },
                },
                // Flow 4 -- Grade Class (required).
                {
                    content: "Select the Grade Class",
                    trigger: ".o_field_many2one[name='grade_class_id'] input",
                    run: "text TOUR ADM Grade Class",
                },
                {
                    content: "Pick the Grade Class from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR ADM Grade Class)",
                    in_modal: false,
                },
                {
                    content: "Click Create Enrollment in the wizard",
                    trigger: ".modal-footer button[name='action_create_enrollment']",
                },
                {
                    content: "The resulting School Enrollment form opens",
                    trigger:
                        ".o_form_view .o_field_widget[name='student_id']",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission/17-close-addendum.md
    tour.register(
        "ssi_school_admission_school_admission_close_addendum",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Addendum Student"),
            [
                {
                    content: "Open the Fee tab",
                    trigger: ".o_notebook .nav-link:contains(Fee)",
                },
                {
                    // 14.0: a just-opened record is READONLY -- Edit must
                    // be clicked before the "unlocked" litmus gate below
                    // can ever be true (patterns.md §E).
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
                    // Gerbang: before Close Addendum, this row is NOT
                    // readonly yet (patterns.md §P). [name='name'] never
                    // matches: 14.0's list_renderer.js sets only a class
                    // on <td>, never a name attribute.
                    content: "Payment term is unlocked before Close Addendum",
                    trigger:
                        ".o_data_cell.o_list_char[title='TOUR ADM ADDENDUM TERM']:not(.o_readonly_modifier)",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Click Close Addendum",
                    trigger: ".o_form_view button[name='action_close_addendum']",
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Payment term is now locked",
                    trigger:
                        ".o_data_cell.o_list_char[title='TOUR ADM ADDENDUM TERM'].o_readonly_modifier",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Status remains On Progress",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_admission/18-print.md
    tour.register(
        "ssi_school_admission_school_admission_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Print Student"),
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

    // IK: docs/school_admission/19-reload-template-policy.md
    tour.register(
        "ssi_school_admission_school_admission_reload_template_policy",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAdmissionList(),
            openRecordByStudent("TOUR ADM Reload Policy Student"),
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
