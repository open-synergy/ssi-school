# Edit Grade Class

> **Module:** ssi_school\
> **Model:** `school_grade_class`\
> **Menu:** School > Configuration > Grade > Grade Classes\
> **Actor:** user in group `Grade Class`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_generate_code` (Generate Code), `action_reset_code` (Reset
> code)

## Pre-Condition

- **Access:** User is in group `Grade Class`.

## Flow

1. Open the **School > Configuration > Grade > Grade Classes** menu.
2. Find and open the record to edit.
3. Change the required fields (Name, Code, School, Grade, Capacity). Changing **School**
   automatically resets **Grade** to empty and refreshes **Grade Type**.
4. Click **Generate Code** in the header to assign a code from the configured
   `sequence.template`, if the Code field is still **/**. This requires an active
   `sequence.template` for `school_grade_class` — without one, the action fails with an
   error. You may also type the code manually instead.
5. Click **Save**.
6. To make the record eligible for **Generate Code** again, go back to the **Grade
   Classes** list, select the record's checkbox, click **Reset code** in the header,
   then click **OK** to confirm. This resets the Code field back to **/**.

## Post-Condition

- The record is updated with the new values.
