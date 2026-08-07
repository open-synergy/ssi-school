// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_student_graduation.school_student_graduation_batch_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared navigation block reused by every tour below -- corresponds
        // to Flow 1 of every school_student_graduation_batch IK: "Open the
        // School > Student Activities > Graduation Batches menu."
        function openBatchList() {
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
                    content: "Open the Graduation Batches menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_student_graduation.school_student_graduation_batch_menu"]',
                },
                {
                    // Gerbang: tunggu action TUJUAN benar-benar terpasang,
                    // bukan sekadar "ada list di layar" (patterns.md skill
                    // odoo-development-ui-test §A).
                    content: "Graduation Batches list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Graduation Batches)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ];
        }

        // Opens the record identified by the unique Academic Year name
        // shown on the list row (used as Pre-Condition test data marker,
        // since school_student_graduation_batch has no per-record free
        // text field of its own).
        function openRecordByYear(yearName) {
            return [
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(" + yearName + ") .o_data_cell:first",
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

        // Opens the Students tab and clicks Populate Eligible Students
        // (Inline Action documented on 01-create.md / 02-edit.md), then
        // waits for the eligible student to appear in the Lines list.
        function populateEligibleStudents(eligibleStudentName) {
            return [
                {
                    content: "Open the Students tab",
                    trigger: ".o_notebook .nav-link:contains(Students)",
                },
                {
                    content: "Click Populate Eligible Students",
                    trigger:
                        ".o_form_view button[name='action_populate_lines']:enabled",
                },
                {
                    content: "The eligible student appears in the Lines list",
                    trigger:
                        ".o_field_widget[name='line_ids'] .o_data_row:contains(" +
                        eligibleStudentName +
                        ")",
                    run: function () {
                        // Assertion only.
                    },
                },
            ];
        }

        // IK: docs/school_student_graduation_batch/01-create.md
        //
        // Inline Actions: action_populate_lines (Populate Eligible
        // Students) is exercised as a step here, not as its own tour.
        tour.register(
            "ssi_school_student_graduation_school_student_graduation_batch_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Graduation Batches menu.
                openBatchList(),
                [
                    // Flow 2 -- Click the New button. (14.0: "Create")
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
                // Flow 3 -- Date/Academic Year/Academic Term/Grade are all
                // optional (Date defaults to today), so no field needs to
                // be filled before populating.
                //
                // Flow 4 -- On the Students tab, click Populate Eligible
                // Students to fill the Lines list.
                populateEligibleStudents("TOUR SGB Create Eligible Student"),
                [
                    // Flow 5 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },

                    // Post-Condition -- a new record is created in Draft
                    // status.
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

        // IK: docs/school_student_graduation_batch/02-edit.md
        //
        // Inline Actions: action_populate_lines (Populate Eligible
        // Students) is exercised as a step here too.
        tour.register(
            "ssi_school_student_graduation_school_student_graduation_batch_edit",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Graduation Batches menu.
                openBatchList(),
                // Flow 2 -- Find and open the record to edit.
                openRecordByYear("TOUR SGB Edit Year"),
                [
                    // 14.0: a just-opened record is displayed read-only; an
                    // explicit Edit click is required before its fields
                    // become editable. Not itemized in 02-edit.md's Flow --
                    // same documented 14.0 platform mechanic as
                    // school_student_graduation_tour.js test_edit.
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
                // Flow 3/4 -- Refill the Lines list from the current
                // filters via Populate Eligible Students. The batch's
                // Academic Year filter matches only "TOUR SGB Edit
                // Student" (the one line student _create_batch built
                // this record with in Python) -- a differently-scoped
                // "eligible" student would never satisfy this
                // batch's own Populate filter regardless of naming,
                // see test_ui_school_student_graduation_batch.py
                // setUpClass's 02-edit.md comment.
                populateEligibleStudents("TOUR SGB Edit Student"),
                [
                    // Flow 5 -- Click Save. By this point the record is
                    // already persisted -- action_populate_lines is a
                    // type="object" button that implicit-auto-saves before
                    // its RPC runs, and its own write() already landed the
                    // refreshed Lines list, so the form carries no further
                    // dirty state. Confirmed pattern (patterns.md skill
                    // odoo-development-ui-test §P covers the "reload race"
                    // case; this is the sibling "nothing left to save"
                    // case, already fixed the same way in
                    // ssi_school_admission's school_admission_form_tour.js
                    // test_create/test_edit): clicking .o_form_button_save
                    // here fires zero write calls, and 14.0 core does not
                    // transition an already-clean form to .o_form_readonly
                    // -- so that class is NOT a valid gate here. IK
                    // Post-Condition ("The record is updated with the new
                    // values") does not require readonly mode either.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },
                ],
                // Post-Condition -- the record is updated with the new
                // values. Verified by navigating away and re-opening the
                // record (same technique as school_admission_form_tour.js
                // test_edit): the form stayed in edit mode after Save (see
                // note above), and re-opening an EXISTING record always
                // renders it read-only in 14.0, where the Lines list is a
                // reliable, mode-independent kasatmata proof the Populate
                // change actually persisted.
                [
                    {
                        content: "Click the Graduation Batches breadcrumb",
                        trigger:
                            ".breadcrumb-item.o_back_button a:contains(Graduation Batches)",
                    },
                ],
                openRecordByYear("TOUR SGB Edit Year"),
                [
                    {
                        content: "The populated student is still on the record",
                        trigger:
                            ".o_field_widget[name='line_ids'] .o_data_row:contains(TOUR SGB Edit Student)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_student_graduation_batch/03-delete.md
        tour.register(
            "ssi_school_student_graduation_school_student_graduation_batch_delete",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Graduation Batches menu.
                openBatchList(),
                [
                    // Flow 2 -- Select the record to delete (check the
                    // checkbox).
                    {
                        content: "Check the record's selector checkbox",
                        trigger:
                            ".o_data_row:contains(TOUR SGB Delete Year) .o_list_record_selector input",
                    },

                    // Flow 3 -- Click Action > Delete.
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

                    // Flow 4 -- Click OK to confirm.
                    {
                        content: "Confirm deletion",
                        trigger: ".modal-footer button.btn-primary",
                        in_modal: true,
                    },

                    // Post-Condition -- the selected records are
                    // permanently removed from the system.
                    {
                        content: "Record no longer in the list",
                        trigger:
                            ".o_list_view:not(:has(.o_data_row:contains(TOUR SGB Delete Year)))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_student_graduation_batch/04-confirm.md
        tour.register(
            "ssi_school_student_graduation_school_student_graduation_batch_confirm",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Graduation Batches menu.
                openBatchList(),
                // Flow 2 -- Open the record to confirm.
                openRecordByYear("TOUR SGB Confirm Year"),
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

                    // Post-Condition -- status changes to Waiting for
                    // Approval.
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

        // IK: docs/school_student_graduation_batch/05-approve.md
        tour.register(
            "ssi_school_student_graduation_school_student_graduation_batch_approve",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Graduation Batches menu.
                openBatchList(),
                // Flow 2 -- Open the record to approve.
                openRecordByYear("TOUR SGB Approve Year"),
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

                    // Post-Condition -- the single approval level is
                    // fulfilled, so status changes automatically to Done
                    // (there is no separate manual Finish step for this
                    // model).
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

        // IK: docs/school_student_graduation_batch/06-reject.md
        tour.register(
            "ssi_school_student_graduation_school_student_graduation_batch_reject",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Graduation Batches menu.
                openBatchList(),
                // Flow 2 -- Open the record to reject.
                openRecordByYear("TOUR SGB Reject Year"),
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

        // IK: docs/school_student_graduation_batch/10-cancel.md
        tour.register(
            "ssi_school_student_graduation_school_student_graduation_batch_cancel",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Graduation Batches menu.
                openBatchList(),
                // Flow 2 -- Open the record to cancel.
                openRecordByYear("TOUR SGB Cancel Year"),
                [
                    // Flow 3 -- Click the Cancel button.
                    {
                        content: "Click the Cancel button",
                        trigger:
                            ".o_statusbar_buttons button:enabled:contains('Cancel')",
                        extra_trigger: ".o_form_view",
                    },
                    {
                        content: "Wizard is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 4 -- In the wizard, select the Cancellation
                    // Reason (radio widget).
                    {
                        content: "Select the cancellation reason",
                        trigger:
                            ".o_field_widget[name='cancel_reason_id'] " +
                            ".o_radio_item:contains(TOUR SGB Cancel Reason) input",
                        run: "click",
                    },

                    // Flow 5 -- Click Confirm.
                    {
                        content: "Confirm the wizard",
                        trigger: ".modal-footer button[name='action_confirm']",
                    },

                    // Flow 6 -- Click OK on the confirmation dialog.
                    {
                        content: "Confirm the Are you sure? dialog",
                        trigger: ".modal-footer button.btn-primary",
                        in_modal: true,
                    },

                    // Post-Condition -- status changes to Cancelled.
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

        // IK: docs/school_student_graduation_batch/12-restart.md
        tour.register(
            "ssi_school_student_graduation_school_student_graduation_batch_restart",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Graduation Batches menu.
                openBatchList(),
                // Flow 2 -- Open the record to restart.
                openRecordByYear("TOUR SGB Restart Year"),
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

        // IK: docs/school_student_graduation_batch/13-reset-number.md
        tour.register(
            "ssi_school_student_graduation_school_student_graduation_batch_reset_number",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Graduation Batches menu.
                openBatchList(),
                // Flow 2 -- Open the record whose document number will be
                // reset.
                openRecordByYear("TOUR SGB Reset Number Year"),
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

                    // Post-Condition -- document number returns to "/".
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

        // IK: docs/school_student_graduation_batch/14-restart-approval.md
        //
        // Config Pre-Condition note: same shape as
        // school_student_graduation -- policy_template/school_student_
        // graduation_batch.xml does not ship a policy.template_detail
        // granting restart_approval_ok, so the test file's setUpClass
        // supplies it directly.
        tour.register(
            "ssi_school_student_graduation_school_student_graduation_batch_restart_approval",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Graduation Batches menu.
                openBatchList(),
                // Flow 2 -- Open the record whose approval process is
                // stalled.
                openRecordByYear("TOUR SGB Restart Approval Year"),
                [
                    // Flow 3 -- Click the Restart Approval Process button.
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

                    // Post-Condition -- status remains Waiting for
                    // Approval.
                    {
                        content: "Status is still Waiting for Approval",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_student_graduation_batch/15-print.md
        //
        // Boundary (patterns.md §Q): see school_student_graduation_tour.js
        // test_print for the same reasoning -- the tour only proves the
        // wizard opens then closes it, without printing.
        tour.register(
            "ssi_school_student_graduation_school_student_graduation_batch_print",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Graduation Batches menu.
                openBatchList(),
                // Flow 2 -- Open the record to print.
                openRecordByYear("TOUR SGB Print Year"),
                [
                    // Flow 3 -- Click Print in the header.
                    {
                        content: "Click the Print button",
                        trigger:
                            ".o_statusbar_buttons button:enabled:contains('Print')",
                        extra_trigger: ".o_form_view",
                    },

                    // Flow 4/5 boundary -- the wizard is proven open, then
                    // closed.
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

                    // Post-Condition (tour boundary) -- the wizard is
                    // closed and the record form is displayed again.
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

        // IK: docs/school_student_graduation_batch/16-reload-template-policy.md
        //
        // Boundary: same reasoning as school_student_graduation_tour.js
        // test_reload_template_policy -- no dialog/notification signal;
        // the tour only proves the button is reachable and clickable.
        tour.register(
            "ssi_school_student_graduation_school_student_graduation_batch_reload_template_policy",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Graduation Batches menu.
                openBatchList(),
                // Flow 2 -- Open the record whose assigned policy template
                // should be re-evaluated.
                openRecordByYear("TOUR SGB Reload Policy Year"),
                [
                    // Flow 3 -- On the Policies tab, click Reload Template
                    // Policy.
                    {
                        content: "Open the Policies tab",
                        trigger: ".o_notebook .nav-link:contains(Policies)",
                    },
                    {
                        content: "Click the Reload Template Policy button",
                        trigger:
                            ".o_form_view button[name='action_reload_policy_template']:enabled",
                    },

                    // Post-Condition (tour boundary) -- the form survives
                    // the click.
                    {
                        content: "Form is intact after the reload",
                        trigger: "body:not(.o_ui_blocked)",
                        extra_trigger:
                            ".o_form_view button[name='action_reload_policy_template']:enabled",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
