# Edit Grade

> **Module:** ssi_school\
> **Model:** `school_grade`\
> **Menu:** School > Configuration > Grade > Grades\
> **Actor:** user in group `Grade`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_generate_code` (Generate Code), `action_reset_code` (Reset
> code)

## Pre-Condition

- **Access:** User is in group `Grade`.

## Flow

1. Open the **School > Configuration > Grade > Grades** menu.
2. Find and open the record to edit.
3. Change the required fields (Name, Code, Type, Sequence).
4. Click **Generate Code** in the header to assign a code from the configured
   `sequence.template`, if the Code field is still **/**. This requires an active
   `sequence.template` for `school_grade` — without one, the action fails with an error.
   You may also type the code manually instead.
5. Click **Save**. Changing **Type** or **Sequence** automatically recomputes **Previous
   Grade** and **Next Grade** for every Grade of the affected Type(s).
6. To make the record eligible for **Generate Code** again, go back to the **Grades**
   list, select the record's checkbox, click **Reset code** in the header, then click
   **OK** to confirm. This resets the Code field back to **/**.

## Post-Condition

- The record is updated with the new values.
