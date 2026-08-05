# Create Invoice Export — Admission

> **Module:** ssi*school_admission_customer_invoice_export\
> **Model:** `school_admission`\
> **Extends:** ssi_school_admission — model `school_admission`\
> **Menu:** School > Admission > Admissions\
> **Actor:** user in group \_Admission — User*\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress** or **Done**.
- **Record:** At least one Payment Terms line has an unpaid (**Open**) Customer Invoice
  that already carries a posted journal entry.
- **Data:** At least one active Customer Invoice Export Type exists
  (`ssi_customer_invoice_export/customer_invoice_export_type/01-create`).
- **Config:** An active `policy.template` for this model grants
  `create_invoice_export_ok` for state `open` or `done` to the actor's group.
- **Access:** User is in group _Admission — User_.

## Flow

1. Open the **School > Admission > Admissions** menu.
2. Open the record whose unpaid invoices will be exported.
3. Click the **Create Invoice Export** button
   (`action_open_create_invoice_export_wizard`).
4. In the **Create Invoice Export** wizard, the current record is pre-selected (kept in
   a hidden field, not shown in the form).
5. Fill in the fields:
   - **Type** _(required)_: select the Customer Invoice Export Type. Selecting a Type
     proposes its default **Output Format**.
   - **Date** _(required)_: defaults to today's date. Change if needed.
   - **Output Format** _(required)_: automatically filled from **Type**; change if
     needed.
   - **Date Start**: optional. Lower bound (inclusive) on invoice date, passed as-is to
     the resulting document. Leave empty for no lower bound.
   - **Date End**: optional. Upper bound (inclusive) on invoice date, passed as-is to
     the resulting document. Leave empty for no upper bound.
6. Click **Create Invoice Export** in the wizard footer
   (`action_create_invoice_export`).

## Post-Condition

- A new **Customer Invoice Export** document is created in **Draft** status, linked to
  the unpaid invoice move(s) collected from this admission's Payment Terms.
- The document's **Invoices**, **Invoice Lines**, and **Summary** tabs are populated
  from those moves, filtered by the selected Type's Product Criteria and grouped by its
  Grouping Method.
- The created document opens in form view.

> **Note:** This wizard can also be run in bulk over several admissions selected from
> the **School > Admission > Admissions** list view, via **Action > Create Invoice
> Export** — every selected admission must individually pass the
> `create_invoice_export_ok` policy, and every admission's unpaid invoices are combined
> into a single Customer Invoice Export document.
