# Edit Admission Payment Template

> **Module:** ssi_school_admission\
> **Model:** `school_admission_payment_template`\
> **Menu:** School > Configuration > Admission > Payment Templates\
> **Actor:** user in group `Admission Payment Template`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_generate_code` (Generate Code), `action_reset_code` (Reset
> code)

## Pre-Condition

- **Access:** User is in group `Admission Payment Template`.

## Flow

1. Open the **School > Configuration > Admission > Payment Templates** menu.
2. Find and open the record to edit.
3. Change the required fields (Name, Code, Academic Term, School, Grade). Changing
   **School** automatically resets **Grade** to empty.
4. Update the Payment Terms, Product Configuration, or Accounting tabs as needed.
5. Click **Generate Code** in the header to assign a code from the configured
   `sequence.template`, if the Code field is still **/**. This requires an active
   `sequence.template` for `school_admission_payment_template` — without one, the action
   fails with an error. You may also type the code manually instead.
6. Click **Save**.
7. To make the record eligible for **Generate Code** again, go back to the **Payment
   Templates** list, select the record's checkbox, click **Reset code** in the header,
   then click **OK** to confirm. This resets the Code field back to **/**.

## Post-Condition

- The record is updated with the new values.
