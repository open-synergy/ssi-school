# Deactivate Grade Type

> **Module:** ssi_school\
> **Model:** `school_grade_type`\
> **Menu:** School > Configuration > Grade > Grade Types\
> **Actor:** user in group `Grade Type`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Grade Type`.

## Flow

1. Open the **School > Configuration > Grade > Grade Types** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated Grade Types cannot be selected in new Grades, Schools, or other records
  that reference a Grade Type.
- Records that already use this Grade Type can still be viewed.
