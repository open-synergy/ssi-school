# Open Enrollment — School Academic Term

> **Module:** ssi_school\
> **Model:** `school_academic_term`\
> **Menu:** School > Configuration > Period > Academic Terms\
> **Actor:** user in group `Academic Term`\
> **State:** `enrollment_state`: `close` → `open`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Enrollment State is **Close**.
- **Access:** User is in group `Academic Term`.

## Flow

1. Open the **School > Configuration > Period > Academic Terms** menu.
2. Open the record to open for enrollment.
3. Click the **Open Enrollment** button.

## Post-Condition

- **Enrollment State** changes to **Open for Enrollment**.
- Students can be enrolled into this Academic Term.
