# Deactivate Branch

> **Module:** ssi_school\
> **Model:** `school_branch`\
> **Menu:** School > Configuration > Branches\
> **Actor:** user in group `Branch`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Branch`.

## Flow

1. Open the **School > Configuration > Branches** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated Branches cannot be selected on new Schools.
- Schools that already use this Branch can still be viewed.
