# Start School Academic Term

> **Module:** ssi_school\
> **Model:** `school_academic_term`\
> **Menu:** School > Configuration > Period > Academic Terms\
> **Actor:** user in group `Academic Term`\
> **State:** `draft` → `open`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Unstarted**.
- **Access:** User is in group `Academic Term`.

## Flow

1. Open the **School > Configuration > Period > Academic Terms** menu.
2. Open the record to start.
3. Click the **Start** button.

## Post-Condition

- Status changes to **On progress**.
