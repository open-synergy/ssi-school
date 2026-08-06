// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school.school_enrollment_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- corresponds to
    // Flow 1 of every school_enrollment IK: "Open the School > Student
    // Activities > Enrollments menu." "Student Activities" is a level-2
    // menuitem (menu.xml menu_school_student_activity, child of the app
    // root menu_school_root) -- level-2 sections always get their own step
    // regardless of whether they have children, unlike level-3+ grouping
    // headers. "Enrollments" (school_enrollment_menu) is the leaf action.
    function openEnrollmentList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the School app",
                trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
            },
            {
                content: "Open the Student Activities menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
            },
            {
                content: "Open the Enrollments menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.school_enrollment_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang --
                // bukan sekadar "ada list di layar" (patterns.md §A).
                content: "Enrollments list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Enrollments)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
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

    // Opens the record identified by the unique student name shown on the
    // list row's Student column (used as Pre-Condition test data marker --
    // the enrollment's OWN display name is its document number, not the
    // student name, so it cannot be used to find the row).
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

    // IK: docs/school_enrollment/01-create.md
    tour.register(
        "ssi_school_school_enrollment_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            [
                // Flow 2 -- Click the New button.
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
            // Flow 3 -- Fill in the required fields, plus the Payment
            // Template needed to enable Compute Payment below.
            pickMany2one("academic_year_id", "TOUR ENR Academic Year"),
            pickMany2one("academic_term_id", "TOUR ENR Term 1"),
            pickMany2one("school_id", "TOUR ENR School"),
            pickMany2one("grade_id", "TOUR ENR Grade 1"),
            pickMany2one("student_id", "TOUR ENR Create Student"),
            pickMany2one("grade_class_id", "TOUR ENR Class A"),
            pickMany2one("payment_template_id", "TOUR ENR Payment Template"),
            [
                // Flow 4 -- On the Billing tab, click Compute Payment.
                // (Flow 5's per-line Payment Term buttons -- Create/Delete/
                // Disconnect Invoice, Mark/Unmark as Manual, Duplicate --
                // are documented as Inline Actions but are NOT exercised by
                // this tour; see the coordinator report.)
                {
                    content: "Open the Billing tab",
                    trigger: ".o_notebook .nav-link:contains(Billing)",
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
                    content: "Payment Terms are computed from the template",
                    trigger:
                        ".o_field_x2many[name='payment_term_ids'] .o_data_row:contains(TOUR ENR PMT Term)",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 6 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- a new record is created in Draft
                // status, and the Payment Terms tab is filled from the
                // template.
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

    // IK: docs/school_enrollment/02-edit.md
    tour.register(
        "ssi_school_school_enrollment_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Find and open the record to edit.
            openRecordByStudent("TOUR ENR Edit Student"),
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
            // Flow 3 -- Change one of the required fields (Grade Class, to
            // the second homeroom class prepared for this scenario).
            pickMany2one("grade_class_id", "TOUR ENR Class B"),
            pickMany2one("payment_template_id", "TOUR ENR Payment Template"),
            [
                // Flow 4 -- On the Billing tab, click Compute Payment to
                // discard and rebuild the Payment Terms.
                {
                    content: "Open the Billing tab",
                    trigger: ".o_notebook .nav-link:contains(Billing)",
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
                    content: "Payment Terms are rebuilt from the template",
                    trigger:
                        ".o_field_x2many[name='payment_term_ids'] .o_data_row:contains(TOUR ENR PMT Term)",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 6 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- the record is updated with the new
                // values.
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

    // IK: docs/school_enrollment/03-delete.md
    tour.register(
        "ssi_school_school_enrollment_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2/3 -- Open the record, then Action > Delete (delete via
            // the form's Action menu is more reliable in 14.0 than the list
            // checkbox -- patterns.md §I).
            openRecordByStudent("TOUR ENR Delete Student"),
            [
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

                // Flow 4 -- Click OK to confirm.
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // After delete, 14.0 may show the next record in the list
                // instead of navigating back on its own -- return
                // explicitly via the breadcrumb.
                {
                    content: "Click the Enrollments breadcrumb",
                    trigger: ".breadcrumb-item.o_back_button a:contains(Enrollments)",
                },

                // Post-Condition -- the record is permanently removed.
                {
                    content: "Record no longer in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR ENR Delete Student)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_enrollment/04-confirm.md
    tour.register(
        "ssi_school_school_enrollment_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record to confirm.
            openRecordByStudent("TOUR ENR Confirm Student"),
            [
                // Flow 3 -- Click the Confirm button.
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Waiting for Approval.
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

    // IK: docs/school_enrollment/05-approve.md
    tour.register(
        "ssi_school_school_enrollment_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record to approve.
            openRecordByStudent("TOUR ENR Approve Student"),
            [
                // Flow 3 -- Click the Approve button.
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- the single approval level is fulfilled,
                // status automatically changes to On Progress (there is no
                // separate Start step for this model).
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

    // IK: docs/school_enrollment/06-reject.md
    tour.register(
        "ssi_school_school_enrollment_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record to reject.
            openRecordByStudent("TOUR ENR Reject Student"),
            [
                // Flow 3 -- Click the Reject button.
                {
                    content: "Click the Reject button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reject_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Rejected.
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

    // IK: docs/school_enrollment/09-finish.md
    tour.register(
        "ssi_school_school_enrollment_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record to finish.
            openRecordByStudent("TOUR ENR Finish Student"),
            [
                // Flow 3 -- Click the Done button.
                {
                    content: "Click the Done button",
                    trigger: ".o_statusbar_buttons button[name='action_done']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Done.
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

    // IK: docs/school_enrollment/10-cancel.md
    tour.register(
        "ssi_school_school_enrollment_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record to cancel.
            openRecordByStudent("TOUR ENR Cancel Student"),
            [
                // Flow 3 -- Click the Cancel button (opens the reason
                // wizard; the rendered button name is a numeric action id,
                // so match by label instead of button[name=...] --
                // selectors.md §4).
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                    extra_trigger: ".o_form_view",
                },
                {
                    // 14.0: JANGAN prefiks `.modal` -- trigger dicari DI
                    // DALAM modal, jadi `.o_form_view` saja (patterns.md
                    // §H).
                    content: "Wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 4 -- In the wizard, select the Cancellation Reason
                // (radio widget).
                {
                    content: "Select the cancellation reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] " +
                        ".o_radio_item:contains(TOUR ENR Cancel Reason) input",
                    run: "click",
                },

                // Flow 5 -- Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },
                {
                    // The wizard's own Confirm button carries a "Are you
                    // sure?" confirm attribute, stacking a second dialog on
                    // top; $modal_displayed now resolves to that topmost
                    // dialog.
                    content: "Confirm the Are you sure? dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Flow 6 -- Post-Condition -- status changes to Cancelled.
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

    // IK: docs/school_enrollment/12-restart.md
    tour.register(
        "ssi_school_school_enrollment_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record to restart.
            openRecordByStudent("TOUR ENR Restart Student"),
            [
                // Flow 3 -- Click the Restart button.
                {
                    content: "Click the Restart button",
                    trigger: ".o_statusbar_buttons button[name='action_restart']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status returns to Draft.
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

    // IK: docs/school_enrollment/13-reset-number.md
    tour.register(
        "ssi_school_school_enrollment_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record whose document number will be
            // reset.
            openRecordByStudent("TOUR ENR Reset Number Student"),
            [
                // Flow 3 -- Click the Reset Document Number button.
                {
                    content: "Click the Reset Document Number button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reset_document_number']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- document number returns to "/". After
                // the reset, the form re-renders read-only, so the visible
                // field is "display_name" (not the edit-only "name"
                // field); name_get() renders "/" as "*<id>", which is the
                // observable marker that the reset took effect.
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

    // IK: docs/school_enrollment/14-restart-approval.md
    tour.register(
        "ssi_school_school_enrollment_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record whose approval process is stalled.
            openRecordByStudent("TOUR ENR Restart Approval Student"),
            [
                // Flow 3 -- Click the Restart Approval Process button
                // (name="action_reload_approval_template" -- the button's
                // rendered label is "Restart Approval Process", the method
                // name differs).
                {
                    content: "Click the Restart Approval Process button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reload_approval_template']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status remains Waiting for Approval;
                // the approval process was discarded and rebuilt.
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

    // IK: docs/school_enrollment/15-pass.md
    tour.register(
        "ssi_school_school_enrollment_pass",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record to set as Passed.
            openRecordByStudent("TOUR ENR Pass Student"),
            [
                // Flow 3 -- Click the Pass button
                // (action_set_result_to_passed).
                {
                    content: "Click the Pass button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_set_result_to_passed']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Done.
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

    // IK: docs/school_enrollment/16-fail.md
    tour.register(
        "ssi_school_school_enrollment_fail",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record to set as Failed.
            openRecordByStudent("TOUR ENR Fail Student"),
            [
                // Flow 3 -- Click the Fail button
                // (action_set_result_to_failed).
                {
                    content: "Click the Fail button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_set_result_to_failed']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Done.
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

    // IK: docs/school_enrollment/17-drop-out.md
    tour.register(
        "ssi_school_school_enrollment_drop_out",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record to set as Drop Out.
            openRecordByStudent("TOUR ENR Drop Out Student"),
            [
                // Flow 3 -- Click the Drop Out button
                // (action_set_result_to_drop_out).
                {
                    content: "Click the Drop Out button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_set_result_to_drop_out']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Done.
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

    // IK: docs/school_enrollment/18-graduate.md
    tour.register(
        "ssi_school_school_enrollment_graduate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record to set as Graduate.
            openRecordByStudent("TOUR ENR Graduate Student"),
            [
                // Flow 3 -- Click the Graduate button
                // (action_set_result_to_graduate).
                {
                    content: "Click the Graduate button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_set_result_to_graduate']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Done.
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

    // IK: docs/school_enrollment/19-create-due-invoice.md
    tour.register(
        "ssi_school_school_enrollment_create_due_invoice",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record whose due Payment Terms will be
            // invoiced.
            openRecordByStudent("TOUR ENR Invoice Student"),
            [
                // Flow 3 -- Click the Create Due Invoice button
                // (action_open_create_due_invoice_wizard).
                {
                    content: "Click the Create Due Invoice button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_open_create_due_invoice_wizard']",
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

                // Flow 4 -- the current record is pre-selected in
                // Enrollments (readonly many2many tags, no interaction
                // needed).
                // Flow 5 -- leave Date Start / Date End empty (no lower
                // bound; process up to today).

                // Flow 6 -- Click Create Due Invoice in the wizard footer.
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

                // Post-Condition -- the due Payment Term becomes Invoiced.
                {
                    content: "Open the Billing tab",
                    trigger: ".o_notebook .nav-link:contains(Billing)",
                },
                {
                    content: "Payment term status is now Invoiced",
                    trigger:
                        ".o_data_row:contains(TOUR ENR DUE TERM) .o_field_cell[name='state']:contains(Invoiced)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_enrollment/20-close-addendum.md
    tour.register(
        "ssi_school_school_enrollment_close_addendum",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record whose addendum Payment Terms will
            // be locked.
            openRecordByStudent("TOUR ENR Addendum Student"),
            [
                {
                    content: "Open the Billing tab",
                    trigger: ".o_notebook .nav-link:contains(Billing)",
                },
                {
                    // Gerbang: sebelum Close Addendum, baris ini BELUM
                    // readonly -- uji lakmus patterns.md §P terpenuhi
                    // (selector tidak cocok bila aksi belum dijalankan).
                    content: "Payment term is unlocked before Close Addendum",
                    trigger:
                        ".o_data_row:contains(TOUR ENR ADDENDUM TERM) .o_field_cell[name='name']:not(.o_readonly_modifier)",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 -- On the Billing tab, click Close Addendum
                // (action_close_addendum).
                {
                    content: "Click Close Addendum",
                    trigger: ".o_form_view button[name='action_close_addendum']",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status remains On Progress; the
                // previously-unlocked payment term becomes locked
                // (read-only) in the Payment Terms tree.
                {
                    content: "Payment term is now locked",
                    trigger:
                        ".o_data_row:contains(TOUR ENR ADDENDUM TERM) .o_field_cell[name='name'].o_readonly_modifier",
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

    // IK: docs/school_enrollment/21-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the button opens
    // the "Select Report To Print" wizard, then closes it via Cancel. It
    // never selects a report nor clicks the wizard's own Print button,
    // because the resulting report action is an ir.actions.act_url
    // download with no DOM "finished" signal -- clicking through it could
    // hang headless Chrome.
    tour.register(
        "ssi_school_school_enrollment_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record to print.
            openRecordByStudent("TOUR ENR Print Student"),
            [
                // Flow 3 -- Click Print in the header. The button is
                // injected by ssi_print_mixin as type="action" -- its
                // ``name`` attribute is a numeric action id resolved at
                // render time, so it must be targeted by its visible label
                // (selectors.md §4), not by ``[name=...]``.
                {
                    content: "Click the Print button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Print')",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4/5 boundary -- the wizard is proven open, then
                // closed. Selecting the report/Type and clicking the
                // wizard's own Print button are intentionally NOT
                // executed -- see the module docstring above.
                {
                    // 14.0: JANGAN prefiks `.modal` (patterns.md §H).
                    content: "The Select Report To Print wizard is displayed",
                    trigger: ".modal-title:contains('Select Report To Print')",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Close the wizard",
                    // The button carries the "special" attribute, which
                    // survives the form renderer's class mapping and is the
                    // stable anchor.
                    trigger: ".modal-footer button[special='cancel']",
                    in_modal: true,
                },

                // Post-Condition (tour boundary) -- the wizard is closed
                // and the enrollment form is displayed again. Whether a
                // report is actually generated and downloaded is out of
                // tour scope.
                {
                    content: "Wizard is closed and the enrollment form is displayed",
                    trigger: ".o_form_view",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_enrollment/22-reload-template-policy.md
    tour.register(
        "ssi_school_school_enrollment_reload_template_policy",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            // Flow 2 -- Open the record whose assigned policy template
            // should be re-evaluated (Pre-Condition: policy_template_id
            // was cleared beforehand, so this proves an observable
            // before/after change).
            openRecordByStudent("TOUR ENR Reload Policy Student"),
            [
                {
                    content: "Open the Policies tab",
                    trigger: ".o_notebook .nav-link:contains(Policies)",
                },

                // Flow 3 -- Click Reload Template Policy.
                {
                    content: "Click Reload Template Policy",
                    trigger: "button[name='action_reload_policy_template']",
                },

                // Post-Condition -- Policy Template is recomputed and
                // re-assigned (the field goes from empty to "Standard").
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

    // IK: docs/school_enrollment/24-copy-payment-term.md
    tour.register(
        "ssi_school_school_enrollment_copy_payment_term",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Enrollments menu.
            openEnrollmentList(),
            [
                // Flow 2 -- In the list view, tick the checkbox of the
                // enrollment that will receive the payment terms.
                {
                    content: "Select the target enrollment",
                    trigger:
                        ".o_data_row:contains(TOUR ENR Copy Target Student) .o_list_record_selector input",
                    run: "click",
                },

                // Flow 3 -- Click Action > Copy Payment Terms.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Copy Payment Terms",
                    // Match the exact label, not a substring (patterns.md
                    // §I).
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $item = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return $(this).text().trim() === "Copy Payment Terms";
                            }
                        );
                        $item[0].click();
                    },
                },
                {
                    // 14.0: JANGAN prefiks `.modal` (patterns.md §H).
                    content: "Wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 4 -- the ticked target is shown read-only in Target
                // Enrollments (no interaction needed).

                // Flow 5 -- fill Source Enrollment. Mode keeps its Replace
                // default (a pre-selected radio option, per patterns.md
                // §C's "fill enough to save" boundary).
                {
                    content: "Select the Source Enrollment field value",
                    trigger: ".o_field_many2one[name='source_enrollment_id'] input",
                    run: "text TOUR-ENR-COPY-SOURCE-001",
                },
                {
                    content: "Pick the source from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-ENR-COPY-SOURCE-001)",
                    in_modal: false,
                },

                // Flow 6 -- Click Copy Payment Terms in the wizard footer.
                {
                    content: "Click Copy Payment Terms in the wizard",
                    trigger: ".modal-footer button[name='action_copy_payment_term']",
                },
                {
                    content: "Wizard is closed",
                    trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ],
            // Post-Condition -- the target now carries a copy of the
            // source's payment terms.
            openRecordByStudent("TOUR ENR Copy Target Student"),
            [
                {
                    content: "Open the Billing tab",
                    trigger: ".o_notebook .nav-link:contains(Billing)",
                },
                {
                    content: "Copied payment term is present on the target",
                    trigger:
                        ".o_field_x2many[name='payment_term_ids'] .o_data_row:contains(TOUR ENR COPY TERM)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );
});
