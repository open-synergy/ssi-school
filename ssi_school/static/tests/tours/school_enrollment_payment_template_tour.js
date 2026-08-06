// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school.school_enrollment_payment_template_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- corresponds
    // to Flow 1 of every school_enrollment_payment_template IK: "Open
    // the School > Configuration > Enrollment > Payment Templates
    // menu." "Enrollment" is a grouping menuitem with no action of its
    // own (ssi_school/menu.xml menu_enrollment_configuration has no
    // action= attribute and has children), so Odoo 14.0 renders it as a
    // plain, non-clickable "<div class='dropdown-header'>" inside the
    // Configuration dropdown -- NOT as a data-menu-xmlid link. "Payment
    // Templates" is a direct clickable entry inside that SAME dropdown,
    // grouped visually under the "Enrollment" heading -- there is
    // therefore no separate "click Enrollment" step.
    function openPaymentTemplateList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the School app",
                trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_configuration"]',
            },
            {
                content: "Open the Payment Templates menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.school_enrollment_payment_template_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang,
                // bukan sekadar "ada list di layar" (patterns.md §A).
                content: "Payment Templates list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Enrollment Payment Templates)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/school_enrollment_payment_template/01-create.md
    tour.register(
        "ssi_school_school_enrollment_payment_template_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the School > Configuration > Enrollment >
            // Payment Templates menu.
            openPaymentTemplateList(),
            [
                // ── Flow 2 — Click the New button. (14.0: "Create")
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

                // ── Flow 3 — Fill in the required fields: Name, Code.
                // Academic Term, School, Grade, and Default are all
                // optional and left at their defaults (empty / unchecked).
                {
                    content: "Fill in the Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR PMT CREATE",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },

                // ── Flow 4 — On the Payment Terms tab, add one payment
                // period with one fee detail line. The term_ids and
                // detail_ids one2many fields are declared with a
                // <tree> + <form> combo and no editable= attribute
                // (views/school_enrollment_payment_template_views.xml),
                // so "Add a line" opens a FormViewDialog rather than an
                // inline editable row -- confirmed against
                // web/static/src/js/fields/relational_fields.js
                // `_onAddRecord`/`_openFormDialog`. Both the term and
                // detail forms are new (unsaved) records, so their
                // dialog footer's primary button reads "Save & Close"
                // (`multi_select` is true for a new record --
                // view_dialogs.js `FormViewDialog.init`).
                {
                    content: "Open the Payment Terms tab",
                    trigger: ".o_notebook .nav-link:contains(Payment Terms)",
                },
                {
                    content: "Click Add a line on the Payment Terms table",
                    trigger:
                        ".o_field_widget[name='term_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    // 14.0: do NOT prefix the trigger with ".modal" --
                    // $modal_displayed already IS the ".modal" element
                    // (patterns.md §H box).
                    content: "The term dialog is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    // The built-in "text" run helper only dispatches
                    // synthetic keydown/keyup (running_tour_action_
                    // helper.js `_text`) -- it never fires a real
                    // `input` DOM event, so legacy FieldChar's
                    // `_onInput` (basic_fields.js, bound to 'input')
                    // never runs its DEBOUNCED commit to the record's
                    // in-memory data. Normally this is harmless because
                    // `commitChanges()` re-reads the `<input>` element's
                    // raw `.val()` directly at Save time. But here,
                    // adding a row to the NESTED `detail_ids` o2m
                    // (inside this same term dialog, a few steps below)
                    // reloads/re-renders the term dialog's own form,
                    // destroying and recreating this "name" input --
                    // wiping the uncommitted value before Save ever
                    // reads it. Verified in CI: the term dialog's Save
                    // & Close raises "Invalid fields: Term Name" even
                    // though this step reported success. Dispatch a
                    // real `input` event ourselves so the debounced
                    // commit fires immediately, before the nested
                    // dialog can destroy the widget.
                    content: "Fill in the Term Name",
                    trigger: ".o_field_widget[name='name']",
                    run: function () {
                        var el = this.$anchor[0];
                        el.value = "TOUR PMT Term 1";
                        // Match web_tour's own RunningTourActionHelper
                        // `_text` implementation exactly (running_tour_
                        // action_helper.js) -- a genuine native
                        // InputEvent dispatched on the raw DOM element,
                        // not a jQuery-synthesised one, followed by a
                        // native "change" so legacy FieldChar's
                        // `_onChange` (basic_fields.js, NOT debounced)
                        // commits the value to the record immediately.
                        el.dispatchEvent(new InputEvent("input", {bubbles: true}));
                        el.dispatchEvent(new Event("change", {bubbles: true}));
                    },
                },
                {
                    content: "Open the Detail tab in the term dialog",
                    trigger: ".o_notebook .nav-link:contains(Detail)",
                },
                {
                    content: "Click Add a line on the Detail table",
                    trigger:
                        ".o_field_widget[name='detail_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    // A second, nested FormViewDialog opens on top of
                    // the term dialog. $modal_displayed now resolves to
                    // this innermost ".modal:visible:last" -- every
                    // subsequent in-modal trigger below targets it.
                    content: "The detail line dialog is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    // Selecting Product is enough: onchange_name and
                    // onchange_account_id (school_enrollment_payment_
                    // template_term_detail.py) auto-fill Name and
                    // Account from the product, which is prepared in
                    // setUpClass with property_account_income_id set.
                    content: "Select the Product",
                    trigger: ".o_field_many2one[name='product_id'] input",
                    run: "text TOUR PMT PRODUCT",
                },
                {
                    content: "Pick the Product from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR PMT PRODUCT)",
                    in_modal: false,
                },
                {
                    content: "Save & Close the detail line dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    // Gerbang: back to a single modal (the term
                    // dialog) -- the detail line dialog's own root is
                    // gone, so a bare ".o_form_view" here is not a
                    // stale match (uji lakmus patterns.md §A/§P).
                    content: "Detail line dialog is closed",
                    trigger: ".o_field_widget[name='detail_ids'] .o_data_row",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    // Defensive backstop: verified in CI that the term
                    // dialog's Save & Close raised "Invalid fields:
                    // Term Name" even after the earlier fill step
                    // dispatched proper native input/change events --
                    // adding the nested detail_ids row re-renders the
                    // term dialog's form and the Name input can lose
                    // its value in that reload regardless of when it
                    // was committed. Re-fill it now, immediately before
                    // Save, so no further interaction can intervene.
                    content: "Re-confirm the Term Name before saving",
                    trigger: ".o_field_widget[name='name']",
                    run: function () {
                        var el = this.$anchor[0];
                        el.value = "TOUR PMT Term 1";
                        el.dispatchEvent(new InputEvent("input", {bubbles: true}));
                        el.dispatchEvent(new Event("change", {bubbles: true}));
                    },
                },
                {
                    content: "Save & Close the term dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    // Gerbang: back on the main form (no modal left) --
                    // the new term row is now visible in the Payment
                    // Terms table.
                    content: "Term dialog is closed",
                    trigger:
                        ".o_field_widget[name='term_ids'] .o_data_row:contains(TOUR PMT Term 1)",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Flow 5 — On the Product Configuration tab, Product
                // Selection Method keeps its Domain default (only the
                // tab render is verified here).
                {
                    content: "Open the Product Configuration tab",
                    trigger: ".o_notebook .nav-link:contains(Product Configuration)",
                },
                {
                    content: "Product Configuration tab is displayed",
                    trigger: ".o_field_widget[name='product_selection_method']",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Flow 6 — On the Accounting tab, select the
                // required Customer Invoice Type. Receivable Journal,
                // Receivable Account, and Auto Confirm Customer Invoice
                // are optional and left at their defaults.
                {
                    content: "Open the Accounting tab",
                    trigger: ".o_notebook .nav-link:contains(Accounting)",
                },
                {
                    content: "Select the Customer Invoice Type",
                    trigger: ".o_field_many2one[name='customer_invoice_type_id'] input",
                    run: "text TOUR PMT INVOICE TYPE CREATE",
                },
                {
                    content: "Pick the Customer Invoice Type from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR PMT INVOICE TYPE CREATE)",
                    in_modal: false,
                },

                // ── Flow 7 — Click Generate Code in the header.
                {
                    content: "Click Generate Code",
                    trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                    extra_trigger: ".o_form_view",
                },
                {
                    // Gerbang: tombol object di-disable SINKRON saat
                    // diklik dan baru di-enable lagi setelah siklus
                    // auto-save + call_button + reload selesai
                    // (patterns.md §P).
                    content: "Generate Code call has completed",
                    trigger:
                        ".o_statusbar_buttons button[name='action_generate_code']:enabled",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Flow 8 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — A new Enrollment Payment Template
                // record is created and active. (Eligibility for
                // automatic/manual selection on a Homeroom or Enrollment
                // is exercised by those models' own tours, out of this
                // tour's scope.)
                {
                    content:
                        "Enrollment Payment Template record is saved and displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR PMT CREATE)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_enrollment_payment_template/02-edit.md
    tour.register(
        "ssi_school_school_enrollment_payment_template_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Payment Templates menu.
            openPaymentTemplateList(),
            [
                // ── Flow 2 — Find and open the record to edit.
                {
                    content: "Open the record",
                    trigger: ".o_data_row:contains(TOUR PMT EDIT) .o_data_cell:first",
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

                // ── Flow 3 — Change the required fields. (Changing
                // School would automatically reset Grade -- not
                // exercised here, only Name is changed as the
                // representative required field.)
                {
                    content: "Change the Name",
                    trigger: ".o_field_widget[name='name']",
                    run: "text TOUR PMT EDIT CHANGED",
                },

                // ── Flow 4 — Update the Payment Terms, Product
                // Configuration, or Accounting tabs as needed (optional
                // -- not exercised here, see the create tour above for
                // the Payment Terms dialog-editing coverage).

                // ── Flow 5 — Click Generate Code in the header, since
                // the Code field is still "/" (set by setUpClass).
                {
                    content: "Click Generate Code",
                    trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    // Gerbang -- lihat catatan gerbang di tour create
                    // di atas.
                    content: "Generate Code call has completed",
                    trigger:
                        ".o_statusbar_buttons button[name='action_generate_code']:enabled",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Flow 6 — Click Save.
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

                // ── Flow 7 — To make the record eligible for Generate
                // Code again: go back to the Payment Templates list,
                // select the record's checkbox, click Reset code in the
                // header, then click OK to confirm.
                {
                    content: "Click the Enrollment Payment Templates breadcrumb",
                    trigger:
                        ".breadcrumb-item.o_back_button a:contains(Enrollment Payment Templates)",
                },
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:contains(TOUR PMT EDIT CHANGED) .o_list_record_selector input",
                    run: "click",
                },
                {
                    content: "Click Reset code in the list toolbar",
                    trigger: ".o_cp_buttons button[name='action_reset_code']",
                },
                {
                    // Odoo 14.0 core never reads `confirm=` on
                    // <tree><header> bulk-action buttons (only
                    // form/kanban controllers implement it -- verified:
                    // no such handling in list_controller.js or
                    // list_renderer.js). action_reset_code fires
                    // immediately with no dialog; the list then reloads
                    // and clears the row selection, which is a
                    // data-independent proof the RPC landed (the
                    // checkbox is guaranteed checked before this point).
                    content:
                        "Reset Code completes and the list reloads (row selection cleared)",
                    trigger:
                        ".o_data_row:contains(TOUR PMT EDIT CHANGED) .o_list_record_selector input:not(:checked)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Post-Condition — The record is updated with the
                // new values. (Enrollments that already applied this
                // template keep the copied terms/lines -- not a
                // kasatmata UI fact here, out of tour scope.)
                {
                    content: "Reset code dialog is closed",
                    trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_enrollment_payment_template/03-delete.md
    tour.register(
        "ssi_school_school_enrollment_payment_template_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Payment Templates menu.
            openPaymentTemplateList(),
            [
                // ── Flow 2 — Select one or more records to delete
                // (check the checkbox).
                {
                    content: "Select the record to delete",
                    trigger:
                        ".o_data_row:contains(TOUR PMT DELETE) .o_list_record_selector input",
                    run: "click",
                },

                // ── Flow 3 — Click Action > Delete.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Delete",
                    // Item Action menu adalah komponen Owl; cocokkan
                    // LABEL PERSIS (patterns.md §I).
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

                // ── Flow 4 — Click OK to confirm.
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — The selected records, together
                // with their Payment Terms and Detail lines, are
                // permanently removed from the system.
                {
                    content: "Record no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR PMT DELETE)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_enrollment_payment_template/04-deactivate.md
    tour.register(
        "ssi_school_school_enrollment_payment_template_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Payment Templates menu.
            openPaymentTemplateList(),
            [
                // ── Flow 2 — Select one or more records to deactivate
                // (check the checkbox).
                {
                    content: "Select the record to deactivate",
                    trigger:
                        ".o_data_row:contains(TOUR PMT DEACTIVATE) .o_list_record_selector input",
                    run: "click",
                },

                // ── Flow 3 — Click Action > Archive.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Archive",
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $archive = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return $(this).text().trim() === "Archive";
                            }
                        );
                        $archive[0].click();
                    },
                },

                // ── Flow 4 — Click OK to confirm.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — The records are archived and no
                // longer appear in the default list view.
                {
                    content: "Record no longer appears in the active list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR PMT DEACTIVATE)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_enrollment_payment_template/05-activate.md
    tour.register(
        "ssi_school_school_enrollment_payment_template_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Payment Templates menu.
            openPaymentTemplateList(),
            [
                // ── Flow 2 — Enable the Archived filter in the search
                // bar.
                {
                    content: "Open the Filters menu",
                    trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                    run: function () {
                        // Dropdown Owl 14.0 tidak selalu terbuka oleh
                        // klik sintetis default (patterns.md §I/§J).
                        this.$anchor[0].click();
                    },
                },
                {
                    content: "Enable the Archived filter",
                    trigger: ".o_filter_menu .o_menu_item a:contains(Archived)",
                    run: function () {
                        this.$anchor[0].click();
                    },
                },

                // ── Flow 3 — Select one or more records to reactivate
                // (check the checkbox).
                {
                    content: "Select the record to reactivate",
                    trigger:
                        ".o_data_row:contains(TOUR PMT ACTIVATE) .o_list_record_selector input",
                    run: "click",
                },

                // ── Flow 4 — Click Action > Unarchive.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Unarchive",
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $unarchive = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return $(this).text().trim() === "Unarchive";
                            }
                        );
                        $unarchive[0].click();
                    },
                },

                // ── Flow 5 (IK text) -- "Click OK to confirm." Verified
                // against Odoo 14.0 core (list_controller.js
                // `_getActionMenuItems`): only "Archive" wraps its
                // callback in `Dialog.confirm(...)`; "Unarchive" calls
                // `_toggleArchiveState(false)` directly with no
                // confirmation dialog -- known IK inaccuracy, no dialog
                // step added here.
                //
                // Gerbang wajib (patterns.md §P): tanpa ini, langkah
                // berikutnya (buka Filters lalu matikan facet Archived)
                // berlomba dengan RPC action_unarchive yang masih
                // berjalan -- terbukti di CI (race < 25ms, penyebab
                // tour ini gagal). Baris masih tampil di list
                // ter-filter Archived sebelum tombol diklik, jadi
                // begitu unarchive mendarat & list reload, baris ini
                // PASTI hilang dari situ -- gerbang yang sah.
                {
                    content: "Unarchive completes (row leaves the Archived list)",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR PMT ACTIVATE)))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Enabling/disabling the Archived filter re-opens the
                // Filters dropdown.
                {
                    content: "Open the Filters menu again",
                    trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                    run: function () {
                        this.$anchor[0].click();
                    },
                },
                {
                    content: "Disable the Archived filter",
                    trigger: ".o_filter_menu .o_menu_item a:contains(Archived)",
                    run: function () {
                        this.$anchor[0].click();
                    },
                },

                // ── Post-Condition — The records are restored and
                // appear again in the default list view.
                {
                    content: "Record appears again in the active list",
                    trigger: ".o_data_row:contains(TOUR PMT ACTIVATE)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_enrollment_payment_template/06-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the button opens
    // the "Select Report To Print" wizard, then closes it via Cancel. It
    // never selects a report nor clicks the wizard's own Print button,
    // because the resulting report action is an ir.actions.act_url
    // download with no DOM "finished" signal -- clicking through it
    // could hang headless Chrome.
    tour.register(
        "ssi_school_school_enrollment_payment_template_print",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Payment Templates menu.
            openPaymentTemplateList(),
            [
                // ── Flow 2 — Open the record to print.
                {
                    content: "Open the record",
                    trigger: ".o_data_row:contains(TOUR PMT PRINT) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Flow 3 — Click Print in the header. The button is
                // injected by ssi_print_mixin as type="action" -- its
                // `name` attribute is a numeric action id resolved at
                // render time, so it must be targeted by its visible
                // label (selectors.md §4), not by [name=...].
                {
                    content: "Click the Print button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Print')",
                    extra_trigger: ".o_form_view",
                },

                // ── Flow 4/5 boundary — the wizard is proven open, then
                // closed. Selecting the Type/Report Template and
                // clicking the wizard's own Print button are
                // intentionally NOT executed -- see the boundary comment
                // above.
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

                // ── Post-Condition (tour boundary) — the wizard is
                // closed and the Payment Template form is displayed
                // again. Whether a report is actually generated and
                // downloaded is out of tour scope.
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
});
