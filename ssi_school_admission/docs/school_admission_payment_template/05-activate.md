# Activate Admission Payment Template

> **Module:** ssi_school_admission\
> **Model:** `school_admission_payment_template`\
> **Menu:** School > Configuration > Admission > Payment Templates\
> **Actor:** user in group `Admission Payment Template`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group `Admission Payment Template`.

## Flow

1. Open the **School > Configuration > Admission > Payment Templates** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again on new admission records.
