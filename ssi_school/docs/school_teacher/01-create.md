# Create Teacher

> **Module:** ssi_school\
> **Model:** `school_teacher`\
> **Menu:** School > Teachers\
> **Actor:** user in group `Teacher`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** An `hr.employee` record for the person to be registered as a teacher already
  exists.
- **Access:** User is in group `Teacher`.

## Flow

1. Open the **School > Teachers** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the display name of the teacher.
   - **Code** _(required)_: Enter a unique code identifying this teacher, or enter **/**
     to assign it later using **Generate Code**.
   - **Employee** _(required)_: Select the employee record representing this teacher.
     Selecting an Employee synchronizes the **Personal Information**, **Contact &
     Address**, and **Bank Accounts** tabs from the employee's Home Address; every field
     in those tabs is editable directly on the teacher form afterward, and edits are
     written back to the employee's Home Address.
4. On the **Personal Information** tab, review or fill in the identity, birth place,
   health, and socio-cultural fields synchronized from the employee's Home Address.
5. On the **Contact & Address** tab, review or fill in the address and contact fields
   synchronized from the employee's Home Address.
6. On the **Bank Accounts** tab, add lines as needed. Repeat as many times as needed:
   - Click **Add a line**.
   - Fill in **Account Number**, **Bank**, **Account Holder Name**, **Usage**, and
     **Currency**.
7. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school_teacher`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
8. Click **Save**.

## Post-Condition

- A new Teacher record is created and active.
