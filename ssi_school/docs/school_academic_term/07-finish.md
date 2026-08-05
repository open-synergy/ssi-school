# Finish School Academic Term

> **Module:** ssi_school\
> **Model:** `school_academic_term`\
> **Menu:** School > Configuration > Period > Academic Terms\
> **Actor:** user in group `Academic Term`\
> **State:** `open` → `done`\
> **Requires:** `06-start`

## Pre-Condition

- **Record:** Status is **On progress**.
- **Access:** User is in group `Academic Term`.

## Flow

1. Open the **School > Configuration > Period > Academic Terms** menu.
2. Open the record to finish.
3. Click the **Done** button.

## Post-Condition

- Status changes to **Done**.
