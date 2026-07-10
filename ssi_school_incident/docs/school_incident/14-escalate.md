# Escalate School Incident

## Pre-Condition

- Record is in **Open** status.
- At least one active **Incident Escalation Criteria** record exists whose Target Level
  matches the handling tier being escalated to.
- User has _Can Escalate_ access right (belongs to the Officer (Counselor/Vice
  Principal) group or higher).

## Flow

1. Open the **School > Incident > Incidents** menu.
2. Open the School Incident case to escalate.
3. Click the **Escalate** button.
4. In the wizard that appears, fill in:
   - **Target Level**: Select the handling tier this case will be escalated to (Level
     2 - Counselor/Vice Principal, or Level 3 - Principal).
   - **Escalation Criteria**: Select one or more Escalation Criteria whose Target Level
     matches the selected Target Level above, justifying this escalation.
   - **Escalation Reason**: Enter the narrative/chronology explaining why this case is
     being escalated.
5. Click **Escalate** in the wizard footer.

## Post-Condition

- **Handling Level** is updated to the selected Target Level.
- **Resolution Status** becomes **Escalated**.
- **Escalated To Level**, **Escalated By**, and **Escalation Date** are updated to
  reflect this escalation.
- The selected Escalation Criteria and Escalation Reason are recorded on the case.
- A chatter message is posted on the case describing the escalation chronology (target
  level, criteria, and reason).

## Note

- If no Escalation Criteria is selected, or the selected criteria's Target Level does
  not match the Target Level being escalated to, the system shows an error and no change
  is applied.
