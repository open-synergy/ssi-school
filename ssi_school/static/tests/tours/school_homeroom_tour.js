// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school.school_homeroom_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- corresponds to
    // Flow 1 of every school_homeroom IK: "Open the School > Student
    // Activities > Homerooms menu." "Student Activities" is a level-2
    // menuitem that itself has children (Homerooms among them), so it
    // renders as a clickable dropdown-toggle carrying its own
    // data-menu-xmlid (menu.xml), not a plain header. "Homerooms" is the
    // leaf underneath it (views/school_homeroom.xml).
    function openHomeroomList() {
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
                content: "Open the Homerooms menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.school_homeroom_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang, bukan
                // sekadar "ada list di layar" (patterns.md skill
                // odoo-development-ui-test §A).
                content: "Homerooms list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Homerooms)",
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

    // Opens the record identified by its unique Grade Class name, shown
    // as a column on the Homerooms list (a Draft record's own document
    // number is still "/", so it cannot be used as the marker).
    function openRecordByMarker(marker) {
        return [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(" + marker + ") .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/school_homeroom/01-create.md
    tour.register(
        "ssi_school_school_homeroom_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
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
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ],
            // Flow 3 -- Fill in the required fields: Academic Year,
            // Academic Term, School, Grade, Grade Class. Filled in this
            // exact dependency order because each selection clears the
            // next one via onchange (onchange_academic_term_id,
            // onchange_grade_id, onchange_grade_class_id) -- filling
            // upstream to downstream never wipes an already-filled
            // field. Teacher/Date/Capacity are left at their optional /
            // auto-filled defaults, as the IK allows.
            pickMany2one("academic_year_id", "TOUR HR Academic Year"),
            pickMany2one("academic_term_id", "TOUR HR Term 1"),
            pickMany2one("school_id", "TOUR HR School"),
            pickMany2one("grade_id", "TOUR HR Grade"),
            pickMany2one("grade_class_id", "TOUR HR CREATE CLASS"),
            [
                // Flow 5 -- Click Save. (Flow 4, selecting Candidate
                // Students on the Generate Enrollments tab, is an
                // explicit alternative in the IK -- "select manually, OR
                // use 15-fill-random/16-generate-enrollments after
                // saving" -- so it is not exercised by this tour.)
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
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/02-edit.md
    tour.register(
        "ssi_school_school_homeroom_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Find and open the record to edit.
            openRecordByMarker("TOUR HR EDIT CLASS"),
            [
                // Flow 3 -- Change one of the required fields (Grade
                // Class). Candidate Students add/remove on the Generate
                // Enrollments tab (Flow 4) is worded "as needed" in the
                // IK -- it is optional and not exercised by this tour.
                {
                    content: "Click the Edit button",
                    trigger: ".o_form_button_edit",
                },
                {
                    content: "Form is now editable",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ],
            pickMany2one("grade_class_id", "TOUR HR EDIT CLASS B"),
            [
                // Flow 5 -- Click Save.
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
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/03-delete.md
    tour.register(
        "ssi_school_school_homeroom_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            [
                // Flow 2 -- Select the record to delete (check the
                // checkbox), from the LIST -- the IK documents this as a
                // checkbox+Action-menu flow, not a form-based delete.
                {
                    content: "Check the record checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR HR DELETE CLASS) " +
                        ".o_list_record_selector input",
                    extra_trigger: ".o_list_view",
                },

                // Flow 3 -- Click Action > Delete.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                    // Dropdown Owl di 14.0 tidak selalu terbuka oleh klik
                    // sintetis default (patterns.md skill
                    // odoo-development-ui-test §I).
                    run: function () {
                        this.$anchor[0].click();
                    },
                },
                {
                    content: "Click Delete",
                    // Cocokkan LABEL PERSIS -- :contains(Delete) sebagai
                    // substring bisa keliru menunjuk item lain.
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

                // Post-Condition -- the selected record is permanently
                // removed from the system.
                {
                    content: "Record no longer in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR HR DELETE CLASS)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/04-confirm.md
    tour.register(
        "ssi_school_school_homeroom_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Open the record to confirm.
            openRecordByMarker("TOUR HR CONFIRM CLASS"),
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
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/05-approve.md
    tour.register(
        "ssi_school_school_homeroom_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Open the record to approve.
            openRecordByMarker("TOUR HR APPROVE CLASS"),
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
                // fulfilled, so status changes automatically to On
                // Progress (there is no separate Start step for this
                // model -- see the note in 05-approve.md).
                {
                    content: "Status is On Progress",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/06-reject.md
    tour.register(
        "ssi_school_school_homeroom_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Open the record to reject.
            openRecordByMarker("TOUR HR REJECT CLASS"),
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
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/09-finish.md
    tour.register(
        "ssi_school_school_homeroom_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Open the record to finish.
            openRecordByMarker("TOUR HR FINISH CLASS"),
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
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/10-cancel.md
    tour.register(
        "ssi_school_school_homeroom_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Open the record to cancel.
            openRecordByMarker("TOUR HR CANCEL CLASS"),
            [
                // Flow 3 -- Click the Cancel button (opens the reason
                // wizard; the rendered button name is a numeric action
                // id, so match by label instead of button[name=...] --
                // selectors.md skill odoo-development-ui-test §4).
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                    extra_trigger: ".o_form_view",
                },
                {
                    // 14.0: JANGAN prefiks `.modal` -- trigger dicari DI
                    // DALAM modal, jadi `.o_form_view` saja (patterns.md
                    // skill odoo-development-ui-test §H).
                    content: "Wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },

                // Flow 4 -- In the wizard, select the Cancellation
                // Reason (radio widget).
                {
                    content: "Select the cancellation reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] " +
                        ".o_radio_item:contains(TOUR HR Cancel Reason) input",
                    run: "click",
                },

                // Flow 5 -- Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // Flow 6 -- Click OK on the confirmation dialog (the
                // wizard's own Confirm button carries a "Are you sure?"
                // confirm attribute, stacking a second dialog on top).
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
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/12-restart.md
    tour.register(
        "ssi_school_school_homeroom_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Open the record to restart.
            openRecordByMarker("TOUR HR RESTART CLASS"),
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

                // Post-Condition -- status returns to Draft. (Approval
                // records being removed and the approval template
                // cleared is not directly observable in the DOM and is
                // unit test territory.)
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/13-reset-number.md
    tour.register(
        "ssi_school_school_homeroom_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Open the record whose document number will be
            // reset.
            openRecordByMarker("TOUR HR RESET NUMBER CLASS"),
            [
                // Flow 3 -- Click the Reset Document Number button (the
                // button variant, not the manual "/" edit alternative).
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
                // After the reset, the form re-renders read-only, so the
                // visible field is "display_name" (not the edit-only
                // "name" field); name_get() renders "/" as "*<id>", which
                // is the observable marker that the reset took effect.
                {
                    content: "Document number is reset (display name shows *)",
                    trigger:
                        ".oe_title .o_field_widget[name='display_name']:contains(*)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/14-restart-approval.md
    tour.register(
        "ssi_school_school_homeroom_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Open the record whose approval process is
            // stalled.
            openRecordByMarker("TOUR HR RESTART APPROVAL CLASS"),
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
                // (The old approval records being discarded and a new
                // process being created from the approval template is
                // not directly observable in the DOM and is unit test
                // territory.)
                {
                    content: "Status is still Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: "body:not(.o_ui_blocked)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/15-fill-random.md
    tour.register(
        "ssi_school_school_homeroom_fill_random",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Open the record to fill.
            openRecordByMarker("TOUR HR FILL RANDOM CLASS"),
            [
                // Flow 3 -- On the Generate Enrollments tab, click the
                // Fill Random button.
                {
                    content: "Open the Generate Enrollments tab",
                    trigger: ".o_notebook .nav-link:contains(Generate Enrollments)",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "The Fill Random button is displayed and enabled",
                    trigger: ".o_form_view button[name='action_fill_random']:enabled",
                    extra_trigger:
                        ".o_notebook .nav-link.active:contains(Generate Enrollments)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Click the Fill Random button",
                    trigger: ".o_form_view button[name='action_fill_random']",
                },

                // Post-Condition -- Candidate Students is filled with a
                // RANDOM selection of eligible students, up to the
                // number of remaining seats (IK: "filled with a random
                // selection of eligible students"). WHICH student gets
                // picked is not guaranteed by the IK and is out of
                // tour scope regardless (a value-level outcome,
                // odoo-development-unit-test territory) -- assert only
                // that a row landed, not which one.
                //
                // A specific-name assertion was tried here and proven
                // flaky in CI: setUpClass's _create_grade_class/
                // _create_homeroom/_create_student helpers all share
                // the SAME cls.school/cls.grade across every fixture in
                // this test class, so `allowed_student_ids` (school_id
                // + grade match, state=draft) actually matches BOTH
                // "TOUR HR FILL RANDOM STUDENT" AND "TOUR HR GENERATE
                // STUDENT" (school_homeroom.py
                // _compute_allowed_student_ids) -- two eligible
                // candidates for Capacity 1, so random.sample() (
                // _fill_random_candidate) picks either one with equal
                // probability, and asserting one specific name fails
                // roughly half the time.
                //
                // Gerbang (patterns.md skill odoo-development-ui-test
                // §P): candidate_student_ids is EMPTY before this
                // action runs (Pre-Condition, see setUpClass), so a row
                // appearing here can only happen AFTER Fill Random has
                // run -- it cannot match earlier by coincidence.
                {
                    content: "A candidate student is filled",
                    trigger:
                        ".o_field_widget[name='candidate_student_ids'] .o_data_row",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Status does not change (still Draft)",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/16-generate-enrollments.md
    //
    // Boundary (patterns.md §Q, patterns.md §P): action_generate_
    // enrollments enqueues one queue.job per new candidate via
    // with_delay() to actually create the school_enrollment records.
    // Under the test transaction, that job is never picked up by a
    // runner and never executes, so the created Enrollment can never be
    // observed by this tour (see test_generate_enrollments docstring in
    // tests/test_ui_school_homeroom.py). This tour therefore stops at
    // proving the confirmation dialog appears and the RPC round-trips
    // (status stays On Progress, UI unblocks) -- it never asserts a new
    // Enrollment row.
    tour.register(
        "ssi_school_school_homeroom_generate_enrollments",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Open the record whose enrollments will be
            // generated.
            openRecordByMarker("TOUR HR GENERATE CLASS"),
            [
                // Flow 3 -- On the Generate Enrollments tab, Candidate
                // Students already contains the eligible student
                // (Pre-Condition, prepared in setUpClass) -- no add/
                // adjust is needed here.
                {
                    content: "Open the Generate Enrollments tab",
                    trigger: ".o_notebook .nav-link:contains(Generate Enrollments)",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "The Generate Enrollments button is displayed and enabled",
                    trigger:
                        ".o_form_view button[name='action_generate_enrollments']:enabled",
                    extra_trigger:
                        ".o_notebook .nav-link.active:contains(Generate Enrollments)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },

                // Flow 4 -- Click the Generate Enrollments button.
                {
                    content: "Click the Generate Enrollments button",
                    trigger: ".o_form_view button[name='action_generate_enrollments']",
                },

                // Flow 5 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition (tour boundary) -- status does not
                // change; the record round-trips back to On Progress
                // with the UI unblocked, proving the click completed
                // without error. Whether the background job actually
                // creates the Enrollment is out of tour scope (see the
                // module docstring above).
                {
                    content: "Status does not change (still On Progress)",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                    extra_trigger: "body:not(.o_ui_blocked)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/17-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the button opens
    // the "Select Report To Print" wizard, then closes it via Cancel. It
    // never selects a report nor clicks the wizard's own Print button,
    // because the resulting report action is an ir.actions.act_url
    // download with no DOM "finished" signal -- clicking through it
    // could hang headless Chrome.
    tour.register(
        "ssi_school_school_homeroom_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Open the record to print.
            openRecordByMarker("TOUR HR PRINT CLASS"),
            [
                // Flow 3 -- Click the Print button.
                // The button is injected by ssi_print_mixin as
                // type="action" -- its `name` attribute is a numeric
                // action id resolved at render time, so it must be
                // targeted by its visible label (selectors.md §4), not
                // by [name=...].
                {
                    content: "Click the Print button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Print')",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4/5 boundary -- the wizard is proven open, then
                // closed. Selecting the Type/Report Template and
                // clicking the wizard's own Print button are
                // intentionally NOT executed -- see the module docstring
                // above.
                //
                // 14.0: do NOT prefix the trigger with ".modal" -- when a
                // modal is displayed, web_tour scopes the search to
                // $modal_displayed.find(trigger), and $modal_displayed
                // already IS the ".modal" element.
                {
                    content: "The Select Report To Print wizard is displayed",
                    trigger: ".modal-title:contains('Select Report To Print')",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Close the wizard",
                    // The button is declared with class="oe_link" in the
                    // wizard XML, but the form renderer maps it to
                    // "btn btn-link" in the DOM -- the "special"
                    // attribute survives that mapping and is the stable
                    // anchor.
                    trigger: ".modal-footer button[special='cancel']",
                    in_modal: true,
                },

                // Post-Condition (tour boundary) -- the wizard is closed
                // and the Homeroom form is displayed again. Whether a
                // report is actually generated and downloaded is out of
                // tour scope.
                {
                    content: "Wizard is closed and the Homeroom form is displayed",
                    trigger: ".o_form_view",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_homeroom/18-reload-template-policy.md
    tour.register(
        "ssi_school_school_homeroom_reload_template_policy",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Homerooms menu.
            openHomeroomList(),
            // Flow 2 -- Open the record whose assigned policy template
            // should be re-evaluated. The Pre-Condition record (any
            // status, admin is a member of base.group_system by
            // default) is prepared in setUpClass.
            openRecordByMarker("TOUR HR RELOAD POLICY CLASS"),
            [
                // Flow 3 -- On the Policies tab, click Reload Template
                // Policy.
                {
                    content: "Open the Policies tab",
                    trigger: ".o_notebook .nav-link:contains(Policies)",
                    extra_trigger: ".o_form_view",
                },
                {
                    content:
                        "The Reload Template Policy button is displayed and enabled",
                    trigger:
                        ".o_form_view button[name='action_reload_policy_template']",
                    extra_trigger: ".o_notebook .nav-link.active:contains(Policies)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Click the Reload Template Policy button",
                    trigger:
                        ".o_form_view button[name='action_reload_policy_template']",
                },

                // Post-Condition (tour boundary) -- the Policies tab
                // remains displayed and no error dialog was raised. The
                // resulting policy_template_id value (and the dependent
                // *_ok fields it recomputes) is out of tour scope -- see
                // the Boundary note in test_reload_template_policy's
                // docstring; that is unit test territory.
                {
                    content: "The Policies tab is still displayed, with no error",
                    trigger: ".o_notebook .nav-link.active:contains(Policies)",
                    extra_trigger:
                        "body:not(:has(.modal)) .o_form_view " +
                        "button[name='action_reload_policy_template']",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );
});
