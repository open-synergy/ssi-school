# Restart School Academic Term

> **Module:** ssi_school\
> **Model:** `school_academic_term`\
> **Menu:** School > Configuration > Period > Academic Terms\
> **Actor:** user in group `Academic Term`\
> **State:** `open` | `done` → `draft`\
> **Requires:** `06-start`

## Pre-Condition

- **Record:** Status is **On progress** or **Done**.
- **Access:** User is in group `Academic Term`.

## Flow

1. Open the **School > Configuration > Period > Academic Terms** menu.
2. Open the record to restart.
3. Click the **Restart** button.

## Post-Condition

- Status returns to **Unstarted**.
