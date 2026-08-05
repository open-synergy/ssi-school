# Create Student Leave

> **Module:** ssi*school_student_leave\
> **Model:** `school_student_leave`\
> **Menu:** School > Student Activities > Student Leaves\
> **Actor:** user in group \_School Student Leave — User*\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** The student to be granted leave is currently in the **Enrolled** state
  (`school_student.state = "enrol"`).
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (needed later by `04-confirm`).
- **Access:** User is in group _School Student Leave — User_.

## Flow

1. Open the **School > Student Activities > Student Leaves** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Student** _(required)_: Select the student requesting leave. Must currently be
     **Enrolled**.
   - **Active Enrollment**: Automatically filled, read-only, from the student's
     currently open enrollment.
   - **Academic Term** _(required)_: Select the single academic term this leave is valid
     for.
   - **Date**: Defaults to today's date. Change if needed.
   - **Expected Return Date**: Optional. The date the student is expected to return from
     leave.
   - **Reason**: Optional explanation for the leave request, on the **Leave** tab.
4. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
