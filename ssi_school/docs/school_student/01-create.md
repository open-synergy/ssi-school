# Create Student

> **Module:** ssi_school\
> **Model:** `school_student`\
> **Menu:** School > Students\
> **Actor:** user in group `Student`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** A `res.partner` contact for the student and at least one **School** already
  exist.
- **Access:** User is in group `Student`.

## Flow

1. Open the **School > Students** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the display name of the student.
   - **Code** _(required)_: Enter a unique code identifying this student within its
     School, or enter **/** to assign it later using **Generate Code**.
   - **Contact** _(required)_: Select the contact record representing this student's
     personal data. Selecting a Contact synchronizes the **Personal Information**,
     **Contact & Address**, **Family**, and **Bank Accounts** tabs from the contact;
     every field in those tabs is editable directly on the student form afterward, and
     edits are written back to the linked contact.
4. On the **Personal Information** tab, review or fill in the identity, birth place,
   health, and socio-cultural fields synchronized from the contact.
5. On the **Contact & Address** tab, review or fill in the address and contact fields
   synchronized from the contact.
6. On the **Enrollment** tab:
   - **School** _(required)_: Select the school where this student is enrolling.
   - **Initial Grade Type**: Automatically filled from **School**. Read-only.
   - **Initial Grade**: Select the student's class when first entering school.
     Automatically reset to empty whenever **School** is changed. Optional — used only
     before the student has any enrollment history.
7. On the **Family** tab, review or fill in **Father**, **Mother**, and **Guardian** as
   needed — synchronized from the contact. Optional.
8. On the **Bank Accounts** tab, add lines as needed. Repeat as many times as needed:
   - Click **Add a line**.
   - Fill in **Account Number**, **Bank**, **Account Holder Name**, **Usage**, and
     **Currency**.
9. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school_student`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
10. Click **Save**.

## Post-Condition

- A new Student record is created in the **Waiting for Enrollment** status.
- **Current Grade**, **Current Grade Type**, **Next Grade**, **Active Enrollment**, and
  **Grade Class** are read-only fields, automatically computed from the student's
  enrollment history (initially derived from **Initial Grade**, since no enrollment
  exists yet).
