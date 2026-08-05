# Edit Admission Form

> **Module:** ssi*school_admission\
> **Model:** `school_admission_form`\
> **Menu:** School > Admission > Forms\
> **Actor:** user in group \_Admission Form — User*\
> **Requires:** `01-create`\
> **Inline Actions:** `action_compute_fee` (Compute Fee), `action_compute_tax` (Compute Tax)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Admission Form — User_.

## Flow

1. Open the **School > Admission > Forms** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. On the **Fee Details** tab, click **Compute Fee** to refresh the **Fee Details**
   lines from the selected **Fee Template** — for example after changing the **Fee
   Template**. This replaces any existing fee lines. If skipped, the previously entered
   fee lines are kept unchanged.
5. On the **Accounting** tab, click **Compute Tax** to refresh the **Taxes** lines after
   changing the fee lines or their taxes. If skipped, the **Taxes** tab keeps showing
   stale amounts.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.
