# Deactivate Teacher

> **Module:** ssi_school\
> **Model:** `school_teacher`\
> **Menu:** School > Teachers\
> **Actor:** user in group `Teacher`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Teacher`.

## Flow

1. Open the **School > Teachers** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Records that already reference this Teacher can still be viewed.
