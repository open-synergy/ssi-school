# Evaluate School Academic Alert

> **Module:** ssi*school_incident\
> **Model:** `school_academic_alert`\
> **Menu:** School > Incident > Academic Alerts\
> **Actor:** user in group \_Academic Alert User* or higher\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft** (the status where the _Can Evaluate_ access right
  applies).
- **Access:** User belongs to the Academic Alert User group or higher.

## Flow

1. Open the **School > Incident > Academic Alerts** menu.
2. Open the School Academic Alert record to evaluate.
3. Optionally fill in the **Evaluation Context** field with plain Python assignments to
   seed extra local variables (e.g. `trigger_count = 3`).
4. Click the **Evaluate** button (`action_evaluate`).

The system checks every configured Academic Alert Level from most severe (highest
Sequence, e.g. Red) to least severe (lowest Sequence, e.g. Yellow), running each level's
Python Code against the Student, Subject Note, and any variables seeded by the
Evaluation Context, until one level's Python Code sets `result` to a truthy value.

## Post-Condition

- If a level triggers: **Alert Level** and **Color** are populated with that level's
  values.
- If no level triggers: **Alert Level** is left empty.
- The **Evaluate** button can be clicked again after changing the Evaluation Context to
  re-run the check; the previous Alert Level result is overwritten.
