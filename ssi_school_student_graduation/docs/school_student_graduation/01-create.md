# Create Student Graduation

> **Module:** ssi*school_student_graduation\
> **Model:** `school_student_graduation`\
> **Menu:** School > Student Activities > Student Graduations\
> **Actor:** user in group \_School Student Graduation — User*\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** The student to be graduated is currently in the **Enrolled** state
  (`school_student.state = "enrol"`).
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (needed later by `04-confirm`).
- **Access:** User is in group _School Student Graduation — User_.

## Flow

1. Open the **School > Student Activities > Student Graduations** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Student** _(required)_: Select the student being graduated. Must currently be
     **Enrolled**.
   - **Active Enrollment**: Automatically filled, read-only, from the student's
     currently open enrollment.
   - **Academic Year**: Automatically filled, read-only, from the Active Enrollment.
   - **Academic Term**: Automatically filled, read-only, from the Active Enrollment.
   - **Date**: Defaults to today's date. Change if needed.
   - **Graduation Date**: Optional. The official date the student graduated.
   - **Note**: Optional remarks about this graduation.
4. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
