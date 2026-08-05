# Activate Student

> **Module:** ssi_school\
> **Model:** `school_student`\
> **Menu:** School > Students\
> **Actor:** user in group `Student`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group `Student`.

## Flow

1. Open the **School > Students** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
