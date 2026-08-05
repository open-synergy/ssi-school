# Activate Branch

> **Module:** ssi_school\
> **Model:** `school_branch`\
> **Menu:** School > Configuration > Branches\
> **Actor:** user in group `Branch`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group `Branch`.

## Flow

1. Open the **School > Configuration > Branches** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again on new Schools.
