# Close Enrollment — School Academic Term

> **Module:** ssi_school\
> **Model:** `school_academic_term`\
> **Menu:** School > Configuration > Period > Academic Terms\
> **Actor:** user in group `Academic Term`\
> **State:** `enrollment_state`: `open` → `close`\
> **Requires:** `09-open-enrollment`

## Pre-Condition

- **Record:** Enrollment State is **Open for Enrollment**.
- **Access:** User is in group `Academic Term`.

## Flow

1. Open the **School > Configuration > Period > Academic Terms** menu.
2. Open the record to close for enrollment.
3. Click the **Close Enrollment** button.

## Post-Condition

- **Enrollment State** changes to **Close**.
- New Enrollment records for this Academic Term can no longer be opened — an Enrollment
  cannot move to its **Open** status while the linked Academic Term's Enrollment State is
  **Close**.
