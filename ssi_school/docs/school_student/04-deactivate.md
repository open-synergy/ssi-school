# Deactivate Student

> **Module:** ssi_school\
> **Model:** `school_student`\
> **Menu:** School > Students\
> **Actor:** user in group `Student`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Student`.

## Flow

1. Open the **School > Students** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Records that already reference this Student can still be viewed.
