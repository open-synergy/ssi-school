# Create School Academic Alert

> **Module:** ssi*school_incident\
> **Model:** `school_academic_alert`\
> **Menu:** School > Incident > Academic Alerts\
> **Actor:** user in group \_User (Homeroom Teacher)* or higher\
> **State:** `—` → `draft`

## Pre-Condition

- None.

## Flow

1. Open the **School > Incident > Academic Alerts** menu.
2. Click the **New** button.
3. Fill in the required fields:
   - **Alert Date**: Defaults to today. Change if this academic warning check is being
     performed for a different date.
   - **Student**: Select the student whose academic standing is being evaluated.
   - **Grade Class**: Automatically filled from **Student** (the student's homeroom
     class). Change if needed.
4. Optionally fill in the other fields available in Draft status:
   - **Subject Note**: Enter free-text context, e.g. which subject(s) are below the
     passing grade.
   - **Evaluation Context**: Enter optional Python source (plain assignments only, e.g.
     `trigger_count = 3`) used to seed extra local variables before the Academic Alert
     Level rules run.
5. Click **Save**.

## Post-Condition

- A new School Academic Alert record is created in **Draft** status.
- No Alert Level is set yet: it is only populated after the **Evaluate** button is used.
