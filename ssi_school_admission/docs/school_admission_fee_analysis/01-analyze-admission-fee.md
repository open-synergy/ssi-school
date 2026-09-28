# Analyze Admission Fee

> **Module:** `ssi_school_admission`\
> **Model:** `school_admission_fee_analysis`\
> **Menu:** School > Reporting > Admission Fee Analysis\
> **Actor:** user in group _Admission Fee Analysis_

## Pre-Condition

- **Access:** User is in group _Admission Fee Analysis_ (category _School - Report_).
- **Data:** At least one admission has a payment term with a fee line (detail) that is
  not voided.

## Flow

1. Open the **School > Reporting > Admission Fee Analysis** menu.
2. The report opens in pivot view, with one row per academic year, academic term, and
   product, and the Qty/Untaxed/Tax/Total measures aggregated for those dimensions.

## Post-Condition

- The pivot shows one row per non-voided fee line, aggregated by the displayed
  dimensions. Switching to the list view (top-right view switcher) shows one row per fee
  line instead.
- The search panel offers **Group By** on Academic Year, Academic Term, School, Grade,
  Payment Template, and Product, and **Filters** on the term status
  (Draft/Uninvoiced/Invoiced/Paid) and the admission status (On Progress/Done), to slice
  or narrow the data. The Payment Template dimension also distinguishes the
  Internal/External admission track, since that distinction is encoded in the template
  name.
- The report is read-only: no record can be created, edited, or deleted from this menu.
- A fee line that is voided, or whose detail record is removed, never appears here.
