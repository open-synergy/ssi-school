# Deactivate Admission Payment Template

> **Module:** ssi_school_admission\
> **Model:** `school_admission_payment_template`\
> **Menu:** School > Configuration > Admission > Payment Templates\
> **Actor:** user in group `Admission Payment Template`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Admission Payment Template`.

## Flow

1. Open the **School > Configuration > Admission > Payment Templates** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated templates can no longer be selected on new admission records.
- Admission records that already used this template can still be viewed.
