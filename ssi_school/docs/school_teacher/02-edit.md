# Edit Teacher

> **Module:** ssi_school\
> **Model:** `school_teacher`\
> **Menu:** School > Teachers\
> **Actor:** user in group `Teacher`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_generate_code` (Generate Code), `action_reset_code` (Reset
> code)

## Pre-Condition

- **Access:** User is in group `Teacher`.

## Flow

1. Open the **School > Teachers** menu.
2. Find and open the record to edit.
3. Change the required fields (Name, Code, Employee). Changing **Employee**
   re-synchronizes the **Personal Information**, **Contact & Address**, and **Bank
   Accounts** tabs from the newly selected employee's Home Address.
4. Update the Personal Information, Contact & Address, or Bank Accounts fields as needed
   — changes are written back to the employee's Home Address.
5. Click **Generate Code** in the header to assign a code from the configured
   `sequence.template`, if the Code field is still **/**. This requires an active
   `sequence.template` for `school_teacher` — without one, the action fails with an
   error. You may also type the code manually instead.
6. Click **Save**.
7. To make the record eligible for **Generate Code** again, go back to the **Teachers**
   list, select the record's checkbox, click **Reset code** in the header, then click
   **OK** to confirm. This resets the Code field back to **/**.

## Post-Condition

- The record is updated with the new values.
