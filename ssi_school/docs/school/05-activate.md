# Activate School

> **Module:** ssi_school\
> **Model:** `school`\
> **Menu:** School > Configuration > Grade > Schools\
> **Actor:** user in group `School`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group `School`.

## Flow

1. Open the **School > Configuration > Grade > Schools** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again on new Grade Classes, Students, or Enrollment
  Payment Templates.
