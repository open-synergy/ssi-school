# Activate Academic Year

> **Module:** ssi_school\
> **Model:** `school_academic_year`\
> **Menu:** School > Configuration > Period > Academic Years\
> **Actor:** user in group `Academic Year`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group `Academic Year`.

## Flow

1. Open the **School > Configuration > Period > Academic Years** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again on new records that reference an Academic Year.
