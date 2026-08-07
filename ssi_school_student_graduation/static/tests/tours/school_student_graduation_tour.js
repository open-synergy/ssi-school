// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_student_graduation.school_student_graduation_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- corresponds to
    // Flow 1 of every school_student_graduation IK: "Open the School >
    // Student Activities > Student Graduations menu."
    function openGraduationList() {
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
                content: "Open the Student Graduations menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_student_graduation.school_student_graduation_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang, bukan
                // sekadar "ada list di layar" (patterns.md skill
                // odoo-development-ui-test §A).
                content: "Student Graduations list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Student Graduations)",
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

    // Opens the record identified by the unique Student name shown on the
    // list row (used as Pre-Condition test data marker).
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

    // IK: docs/school_student_graduation/01-create.md
    tour.register(
        "ssi_school_student_graduation_school_student_graduation_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Student Graduations menu.
            openGraduationList(),
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
            // Flow 3 -- Fill in the required field: Student. Active
            // Enrollment / Academic Year / Academic Term are auto-filled,
            // read-only, from the student -- not exercised by clicks here
            // (their auto-fill value is unit test territory).
            pickMany2one("student_id", "TOUR SG Create Student"),
            [
                // Flow 4 -- Click Save.
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

    // IK: docs/school_student_graduation/02-edit.md
    tour.register(
        "ssi_school_student_graduation_school_student_graduation_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Student Graduations menu.
            openGraduationList(),
            // Flow 2 -- Find and open the record to edit.
            openRecordByStudent("TOUR SG Edit Student"),
            [
                // 14.0: a just-opened record is displayed read-only; an
                // explicit Edit click is required before its fields become
                // editable. This step is not itemized in 02-edit.md's Flow
                // -- flagged as a minor IK gap in the task report (compare
                // e.g. ssi_school school_student_mutation_tour.js, which
                // documents the same 14.0 platform mechanic).
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
            // Flow 3 -- Change the required field (Student, from the
            // initial student to a second eligible student).
            pickMany2one("student_id", "TOUR SG Edit Target Student"),
            [
                // Flow 4 -- Click Save.
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

    // IK: docs/school_student_graduation/03-delete.md
    tour.register(
        "ssi_school_student_graduation_school_student_graduation_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Student Graduations menu.
            openGraduationList(),
            [
                // Flow 2 -- Select the record to delete (check the
                // checkbox).
                {
                    content: "Check the record's selector checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR SG Delete Student) .o_list_record_selector input",
                },

                // Flow 3 -- Click Action > Delete.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Delete",
                    // Item Action menu adalah komponen Owl; cocokkan LABEL
                    // PERSIS -- :contains(Delete) sebagai substring bisa
                    // keliru menunjuk item lain. Lihat patterns.md skill
                    // odoo-development-ui-test §I.
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

                // Post-Condition -- the selected records are permanently
                // removed from the system.
                {
                    content: "Record no longer in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR SG Delete Student)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_student_graduation/04-confirm.md
    tour.register(
        "ssi_school_student_graduation_school_student_graduation_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Student Graduations menu.
            openGraduationList(),
            // Flow 2 -- Open the record to confirm.
            openRecordByStudent("TOUR SG Confirm Student"),
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

    // IK: docs/school_student_graduation/05-approve.md
    tour.register(
        "ssi_school_student_graduation_school_student_graduation_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Student Graduations menu.
            openGraduationList(),
            // Flow 2 -- Open the record to approve.
            openRecordByStudent("TOUR SG Approve Student"),
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
                // so status changes automatically to Done (there is no
                // separate manual Finish step for this model).
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

    // IK: docs/school_student_graduation/06-reject.md
    tour.register(
        "ssi_school_student_graduation_school_student_graduation_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Student Graduations menu.
            openGraduationList(),
            // Flow 2 -- Open the record to reject.
            openRecordByStudent("TOUR SG Reject Student"),
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

    // IK: docs/school_student_graduation/10-cancel.md
    tour.register(
        "ssi_school_student_graduation_school_student_graduation_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Student Graduations menu.
            openGraduationList(),
            // Flow 2 -- Open the record to cancel.
            openRecordByStudent("TOUR SG Cancel Student"),
            [
                // Flow 3 -- Click the Cancel button (opens the reason
                // wizard; the rendered button name is a numeric action id,
                // so match by label instead of button[name=...] -- the
                // button is type="action", see selectors.md §4).
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                    extra_trigger: ".o_form_view",
                },
                {
                    // 14.0: JANGAN prefiks `.modal` -- trigger dicari DI
                    // DALAM modal, jadi `.o_form_view` saja. Lihat
                    // patterns.md skill odoo-development-ui-test §H.
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
                        ".o_radio_item:contains(TOUR SG Cancel Reason) input",
                    run: "click",
                },

                // Flow 5 -- Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // Flow 6 -- Click OK on the confirmation dialog. The
                // wizard's Confirm button itself carries a "Are you
                // sure?" confirm attribute, stacking a second dialog on
                // top.
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

    // IK: docs/school_student_graduation/12-restart.md
    tour.register(
        "ssi_school_student_graduation_school_student_graduation_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Student Graduations menu.
            openGraduationList(),
            // Flow 2 -- Open the record to restart.
            openRecordByStudent("TOUR SG Restart Student"),
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

    // IK: docs/school_student_graduation/13-reset-number.md
    tour.register(
        "ssi_school_student_graduation_school_student_graduation_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Student Graduations menu.
            openGraduationList(),
            // Flow 2 -- Open the record whose document number will be
            // reset.
            openRecordByStudent("TOUR SG Reset Number Student"),
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
                // field is "display_name"; name_get() renders "/" as
                // "*<id>", which is the observable marker that the reset
                // took effect.
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

    // IK: docs/school_student_graduation/14-restart-approval.md
    //
    // Config Pre-Condition note: policy_template/school_student_graduation.xml
    // does not ship a policy.template_detail granting restart_approval_ok
    // (a policy field with no matching detail always defaults to False, so
    // the button below would never render). The test file's setUpClass
    // supplies that missing policy.template_detail directly as HttpCase
    // setup data -- exactly the Config Pre-Condition this IK documents.
    tour.register(
        "ssi_school_student_graduation_school_student_graduation_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Student Graduations menu.
            openGraduationList(),
            // Flow 2 -- Open the record whose approval process is stalled.
            openRecordByStudent("TOUR SG Restart Approval Student"),
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

                // Post-Condition -- status remains Waiting for Approval.
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

    // IK: docs/school_student_graduation/15-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the Print button
    // opens the "Select Report To Print" wizard, then closes it via
    // Cancel. It never selects a report nor clicks the wizard's own Print
    // button, because the resulting report action is an
    // ir.actions.act_url download with no DOM "finished" signal --
    // clicking through it could hang headless Chrome.
    tour.register(
        "ssi_school_student_graduation_school_student_graduation_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Student Graduations menu.
            openGraduationList(),
            // Flow 2 -- Open the record to print.
            openRecordByStudent("TOUR SG Print Student"),
            [
                // Flow 3 -- Click Print in the header. The button is
                // injected by ssi_print_mixin as type="action" -- its
                // "name" attribute is a numeric action id resolved at
                // render time, so it must be targeted by its visible
                // label (selectors.md §4), not by [name=...].
                {
                    content: "Click the Print button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Print')",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4/5 boundary -- the wizard is proven open, then
                // closed. Selecting the Report Template and clicking the
                // wizard's own Print button are intentionally NOT
                // executed -- see the boundary note above.
                //
                // 14.0: do NOT prefix the trigger with ".modal" -- when a
                // modal is displayed, web_tour scopes the search to
                // $modal_displayed.find(trigger), and $modal_displayed
                // already IS the ".modal" element (patterns.md §H box).
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

                // Post-Condition (tour boundary) -- the wizard is closed
                // and the record form is displayed again. Whether a
                // report is actually generated and downloaded is out of
                // tour scope.
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

    // IK: docs/school_student_graduation/16-reload-template-policy.md
    //
    // Boundary: action_reload_policy_template (ssi_policy_mixin) writes
    // policy_template_id and returns nothing, so the client just re-reads
    // the record -- there is no dialog, notification, or other kasatmata
    // signal that distinguishes "reassigned" from "already was assigned".
    // This tour therefore only proves the button is reachable on the
    // Policies tab and clickable, and that the form survives the click
    // without error; the actual re-assignment outcome is unit test
    // territory (odoo-development-unit-test).
    tour.register(
        "ssi_school_student_graduation_school_student_graduation_reload_template_policy",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Student Graduations menu.
            openGraduationList(),
            // Flow 2 -- Open the record whose assigned policy template
            // should be re-evaluated.
            openRecordByStudent("TOUR SG Reload Policy Student"),
            [
                // Flow 3 -- On the Policies tab, click Reload Template
                // Policy. The Policies tab itself is always visible; only
                // the inner group holding this button is gated by
                // base.group_system, which the tour's admin login holds
                // by default.
                {
                    content: "Open the Policies tab",
                    trigger: ".o_notebook .nav-link:contains(Policies)",
                },
                {
                    content: "Click the Reload Template Policy button",
                    trigger:
                        ".o_form_view button[name='action_reload_policy_template']:enabled",
                },

                // Post-Condition (tour boundary) -- the form survives the
                // click: the button is still visible and enabled once the
                // client is done processing the reload.
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
});
