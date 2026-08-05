# Deactivate Enrollment Payment Template

> **Module:** ssi_school\
> **Model:** `school_enrollment_payment_template`\
> **Menu:** School > Configuration > Enrollment > Payment Templates\
> **Actor:** user in group `Enrollment Payment Template`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Enrollment Payment Template`.

## Flow

1. Open the **School > Configuration > Enrollment > Payment Templates** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated templates can no longer be selected — manually or automatically (via
  **Default**) — on new Enrollments.
- Enrollments that already applied this template can still be viewed.
