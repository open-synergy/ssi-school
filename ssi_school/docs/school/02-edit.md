# Edit School

> **Module:** ssi_school\
> **Model:** `school`\
> **Menu:** School > Configuration > Grade > Schools\
> **Actor:** user in group `School`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_generate_code` (Generate Code), `action_reset_code` (Reset
> code)

## Pre-Condition

- **Access:** User is in group `School`.

## Flow

1. Open the **School > Configuration > Grade > Schools** menu.
2. Find and open the record to edit.
3. Change the required fields (Name, Code, Grade Type, Center, Branch). Changing
   **Center** automatically clears **Branch** if the currently selected Branch no longer
   belongs to the new Center.
4. Click **Generate Code** in the header to assign a code from the configured
   `sequence.template`, if the Code field is still **/**. This requires an active
   `sequence.template` for `school` — without one, the action fails with an error. You
   may also type the code manually instead.
5. Click **Save**. Saving fails with a validation error if **Branch** is set but its
   Center does not match this school's **Center**.
6. To make the record eligible for **Generate Code** again, go back to the **Schools**
   list, select the record's checkbox, click **Reset code** in the header, then click
   **OK** to confirm. This resets the Code field back to **/**.

## Post-Condition

- The record is updated with the new values.
