# Deactivate Grade

> **Module:** ssi_school\
> **Model:** `school_grade`\
> **Menu:** School > Configuration > Grade > Grades\
> **Actor:** user in group `Grade`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Grade`.

## Flow

1. Open the **School > Configuration > Grade > Grades** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated Grades cannot be selected in new Grade Classes, Student Initial Grade, or
  other records that reference a Grade.
- Records that already use this Grade can still be viewed.
