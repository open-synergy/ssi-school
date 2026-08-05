# Deactivate School

> **Module:** ssi_school\
> **Model:** `school`\
> **Menu:** School > Configuration > Grade > Schools\
> **Actor:** user in group `School`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `School`.

## Flow

1. Open the **School > Configuration > Grade > Schools** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated Schools cannot be selected on new Grade Classes, Students, or Enrollment
  Payment Templates.
- Records that already use this School can still be viewed.
