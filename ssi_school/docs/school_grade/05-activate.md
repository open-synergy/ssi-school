# Activate Grade

> **Module:** ssi_school\
> **Model:** `school_grade`\
> **Menu:** School > Configuration > Grade > Grades\
> **Actor:** user in group `Grade`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group `Grade`.

## Flow

1. Open the **School > Configuration > Grade > Grades** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again in new Grade Classes, Student Initial Grade, or
  other records that reference a Grade.
