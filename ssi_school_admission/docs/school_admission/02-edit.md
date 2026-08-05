# Edit Admission

> **Module:** ssi*school_admission\
> **Model:** `school_admission`\
> **Menu:** School > Admission > Admissions\
> **Actor:** user in group \_Admission — User*\
> **Requires:** `01-create`\
> **Inline Actions:** `action_compute_payment` (Compute Payment), `action_create_invoice`\
> (Create Invoice), `action_delete_invoice` (Delete Invoice),
> `action_disconnect_invoice`\
> (Disconnect Invoice), `action_mark_as_manual` (Mark as Manual), `action_unmark_as_manual`\
> (Unmark as Manual), `action_open_duplicate_wizard` (Duplicate Term)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Admission — User_.

## Flow

1. Open the **School > Admission > Admissions** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. On the **Fee** tab, click **Compute Payment** to refresh the **Payment Terms** lines
   from the selected **Payment Template** — for example after changing the **Payment
   Template**. This replaces any existing payment term lines. If skipped, the previously
   entered payment terms are kept unchanged.
5. Use the payment term row buttons (**Create Invoice**, **Delete Invoice**,
   **Disconnect Invoice**, **Mark as Manual**, **Unmark as Manual**, **Duplicate Term**)
   as needed — same as in `01-create`.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.
