# Edit Student

> **Module:** ssi_school\
> **Model:** `school_student`\
> **Menu:** School > Students\
> **Actor:** user in group `Student`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_generate_code` (Generate Code), `action_reset_code` (Reset
> code)

## Pre-Condition

- **Access:** User is in group `Student`.

## Flow

1. Open the **School > Students** menu.
2. Find and open the record to edit.
3. Change the required fields (Name, Code, Contact, School). Changing **Contact**
   re-synchronizes the **Personal Information**, **Contact & Address**, **Family**, and
   **Bank Accounts** tabs from the newly selected contact. Changing **School**
   automatically resets **Initial Grade** to empty and refreshes **Initial Grade Type**.
4. Update the Personal Information, Contact & Address, Family, Initial Grade, or Bank
   Accounts fields as needed — changes to synchronized fields are written back to the
   linked contact.
5. Click **Generate Code** in the header to assign a code from the configured
   `sequence.template`, if the Code field is still **/**. This requires an active
   `sequence.template` for `school_student` — without one, the action fails with an
   error. You may also type the code manually instead.
6. Click **Save**.
7. To make the record eligible for **Generate Code** again, go back to the **Students**
   list, select the record's checkbox, click **Reset code** in the header, then click
   **OK** to confirm. This resets the Code field back to **/**.

## Post-Condition

- The record is updated with the new values.
