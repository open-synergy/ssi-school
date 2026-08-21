# Edit Academic Alert Level

> **Module:** ssi*school_incident\
> **Model:** `school_academic_alert_level`\
> **Menu:** School > Configuration > Incident > Academic Alert Levels\
> **Actor:** user in group \_Manager (Principal)*\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **School > Configuration > Incident > Academic Alert Levels** menu.
2. Find and open the Academic Alert Level record to edit.
3. Change the required fields (Code, Name, Color, Sequence, Python Code, Action
   Guideline, SLA).
4. Click **Save**.

## Post-Condition

- The Academic Alert Level record is updated with the new values.
- School Academic Alert records already evaluated keep their previously triggered Alert
  Level; only the next Evaluate run picks up the updated rule.
