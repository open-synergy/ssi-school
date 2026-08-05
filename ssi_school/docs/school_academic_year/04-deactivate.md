# Deactivate Academic Year

> **Module:** ssi_school\
> **Model:** `school_academic_year`\
> **Menu:** School > Configuration > Period > Academic Years\
> **Actor:** user in group `Academic Year`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Academic Year`.

## Flow

1. Open the **School > Configuration > Period > Academic Years** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated Academic Years cannot be selected on new records that reference an
  Academic Year (e.g. Academic Term, Enrollment Payment Template).
- Records that already use this Academic Year can still be viewed.
