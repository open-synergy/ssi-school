# Create Incident Escalation Criteria

## Pre-Condition

- None.

## Flow

1. Open the **School > Configuration > Configuration > Escalation Criteria** menu.
2. Click the **New** button.
3. Fill in the required fields:
   - **Code**: Enter a unique code identifying this escalation criterion.
   - **Name**: Enter the name/label of the escalation criterion.
   - **Sequence**: Enter the display/evaluation order of this criterion. Lower values
     are shown/evaluated first. Defaults to 10.
   - **Target Level**: Select the handling tier a case must be escalated to when this
     criterion is met (Level 2 - Counselor/Vice Principal, or Level 3 - Principal).
   - **Verification Method**: Describe how to verify that this escalation criterion has
     been met for a given incident case.
4. Click **Save**.

## Post-Condition

- A new Escalation Criteria record is created and active.
- The new criterion becomes selectable from the Escalation Criteria field of the
  Escalate wizard on a School Incident, filtered by matching Target Level.
