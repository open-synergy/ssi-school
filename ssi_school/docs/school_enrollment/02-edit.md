# Edit Enrollment

> **Module:** ssi*school\
> **Model:** `school_enrollment`\
> **Menu:** School > Student Activities > Enrollments\
> **Actor:** user in group \_Enrollment — User*\
> **Requires:** `01-create`\
> **Inline Actions:** `action_compute_payment` (Compute Payment), `action_create_invoice`
> (Create Invoice), `action_delete_invoice` (Delete Invoice), `action_disconnect_invoice`
> (Disconnect Invoice), `action_mark_as_manual` (Mark as Manual), `action_unmark_as_manual`
> (Unmark as Manual), `action_open_duplicate_wizard` (Duplicate)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Enrollment — User_.

## Flow

1. Open the **School > Student Activities > Enrollments** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. On the **Billing** tab, click **Compute Payment** to discard the current **Payment
   Terms** and rebuild them from the selected **Payment Template** — for example after
   changing the Payment Template or the enrollment Date. Skipping this step leaves the
   existing Payment Terms unchanged.
5. On each Payment Term line, the **Create Invoice**, **Delete Invoice**, **Disconnect
   Invoice**, **Mark as Manual**, **Unmark as Manual**, and **Duplicate** buttons may be
   used the same way as described in `01-create`.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.
