# Create Due Invoice — Enrollment

> **Module:** ssi*school\
> **Model:** `school_enrollment`\
> **Menu:** School > Student Activities > Enrollments\
> **Actor:** user in group \_Enrollment — User*\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Record:** At least one Payment Term is **Uninvoiced** and has an Estimated Invoice
  Date on or before the date range used in the wizard.
- **Config:** An active `policy.template` for this model grants `create_invoice_ok` for
  state `open` to the actor's group.
- **Access:** User is in group _Enrollment — User_.

## Flow

1. Open the **School > Student Activities > Enrollments** menu.
2. Open the record whose due Payment Terms will be invoiced.
3. Click the **Create Due Invoice** button (`action_open_create_due_invoice_wizard`).
4. In the **Create Due Invoice** wizard, the current record is pre-selected in
   **Enrollments**; more enrollments may be added.
5. Fill in the optional fields:
   - **Date Start**: Optional. Lower bound (inclusive) on Estimated Invoice Date. Leave
     empty for no lower bound.
   - **Date End**: Optional. Upper bound (inclusive) on Estimated Invoice Date. Leave
     empty to process up to today.
6. Click **Create Due Invoice** (`action_create_due_invoice`) in the wizard footer.

## Post-Condition

- A customer invoice is created for every Payment Term of the selected enrollment(s)
  that is **Uninvoiced** (Payment Terms marked **Manual** are a separate status and are
  skipped) and has an Estimated Invoice Date within the selected range.
- Each processed Payment Term's status changes to **Invoiced** and is linked to its new
  invoice.
