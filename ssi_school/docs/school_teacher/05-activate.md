# Activate Teacher

> **Module:** ssi_school\
> **Model:** `school_teacher`\
> **Menu:** School > Teachers\
> **Actor:** user in group `Teacher`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group `Teacher`.

## Flow

1. Open the **School > Teachers** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
