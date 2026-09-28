// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_admission.school_admission_fee_analysis_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Flow 1 of docs/school_admission_fee_analysis/01-analyze-admission-fee.md --
    // "Open the School > Reporting > Admission Fee Analysis menu." "Reporting"
    // (menu_school_report, defined in ssi_school) is a level-2 menuitem, so it
    // always gets its own step regardless of how many leaves it has (patterns.md
    // §A). "Admission Fee Analysis" is the level-3 leaf action.
    tour.register(
        "ssi_school_admission_school_admission_fee_analysis_analyze",
        {
            test: true,
            url: "/web",
        },
        [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the School app",
                trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
            },
            {
                content: "Open the Reporting menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_report"]',
            },
            {
                content: "Open the Admission Fee Analysis menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_school_admission.school_admission_fee_analysis_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang, bukan
                // sekadar "ada view di layar" (patterns.md §A).
                content: "Admission Fee Analysis report is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Admission Fee Analysis)",
                extra_trigger: ".o_pivot table",
                run: function () {
                    // Flow 2 -- the pivot renders with at least one row (the
                    // fixture's fee line); no value is asserted here, only
                    // that the report is usable (patterns-post-conditions.md).
                },
            },
        ]
    );
});
