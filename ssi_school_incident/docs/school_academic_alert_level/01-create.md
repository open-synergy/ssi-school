# Create Academic Alert Level

> **Module:** ssi*school_incident\
> **Model:** `school_academic_alert_level`\
> **Menu:** School > Configuration > Incident > Academic Alert Levels\
> **Actor:** user in group \_Manager (Principal)*

## Pre-Condition

- None.

## Flow

1. Open the **School > Configuration > Incident > Academic Alert Levels** menu.
2. Click the **New** button.
3. Fill in the required fields:
   - **Code**: Enter a unique code identifying this alert level.
   - **Name**: Enter the name of the level (e.g. "Yellow - Early Warning").
   - **Color**: Select the warning color of this level (Yellow, Orange, or Red). Only
     Orange and Red levels are allowed to generate a School Incident from a School
     Academic Alert.
   - **Sequence**: Enter the severity ordering (not display ordering) of this level.
     Higher values are evaluated first; the highest-sequence level whose Python Code
     triggers wins (e.g. Red = 30, Orange = 20, Yellow = 10). Defaults to 10.
   - **Python Code**: Enter the Python source, evaluated with safe_eval against the
     School Academic Alert being evaluated, that must set a boolean local variable named
     `result` deciding whether this level is triggered (e.g.
     `result = trigger_count >= 2`).
   - **Action Guideline**: Describe the action the school is required to take when this
     level triggers (who must be notified and what meeting or intervention must follow).
   - **SLA**: Describe the service-level agreement that applies once this level triggers
     (e.g. how soon the parent must be contacted).
4. Click **Save**.

## Post-Condition

- A new Academic Alert Level record is created and active.
- The new level is included in the next Evaluate run of any School Academic Alert, in
  severity (sequence) order.
