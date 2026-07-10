# Create Incident from School Academic Alert

## Pre-Condition

- Record is in **Open** status.
- **Alert Level** is set to an Orange or Red level (from a previous **Evaluate** run).
- User has _Can Create Incident_ access right (belongs to the Officer (Counselor/Vice
  Principal) group or higher).

## Flow

1. Open the **School > Incident > Academic Alerts** menu.
2. Open the School Academic Alert record whose Alert Level is Orange or Red.
3. Click the **Create Incident** button.

## Post-Condition

- A new School Incident record is created, linked back via the **Incident** field on
  this Academic Alert.
- The new School Incident is pre-filled with the Incident Date, Student, Grade Class,
  Incident Type "Academic", Handling Level, and a Description summarizing the alert
  (from Subject Note or the Alert Level's Action Guideline).
- The system opens the newly created School Incident's form view.

## Note

- Attempting **Create Incident** while the Alert Level is empty or set to Yellow shows
  an error and no Incident is created; **Evaluate** the alert first with an Evaluation
  Context that triggers an Orange/Red Academic Alert Level, then try again.
