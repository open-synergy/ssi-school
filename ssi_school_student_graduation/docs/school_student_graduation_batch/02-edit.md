# Edit Graduation Batch

> **Module:** ssi*school_student_graduation\
> **Model:** `school_student_graduation_batch`\
> **Menu:** School > Student Activities > Graduation Batches\
> **Actor:** user in group \_School Student Graduation Batch — User*\
> **Requires:** `01-create`\
> **Inline Actions:** `action_populate_lines` (Populate Eligible Students)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _School Student Graduation Batch — User_.

## Flow

1. Open the **School > Student Activities > Graduation Batches** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. On the **Students** tab, click **Populate Eligible Students** to refill the **Lines**
   list from the current filters (this replaces the current lines), or add/ remove
   student lines manually. At least one line must remain — completing this batch will
   fail without one.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
