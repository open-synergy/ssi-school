# Create Student Profile — Admission

> **Module:** `ssi_school_admission`\
> **Model:** `school_admission`\
> **Menu:** School > Admission > Admissions\
> **Actor:** user in group _Admission — User_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft** or **Waiting for Approval**. This admission's **School
  Student** (**Result** tab) is still empty.
- **Config:** An active `policy.template` for this model grants `create_student_ok` for
  states `draft` and `confirm` to the actor's group.
- **Access:** User is in group _Admission — User_.

## Flow

1. Open the **School > Admission > Admissions** menu.
2. Open the record (status **Draft** or **Waiting for Approval**) to create the student
   profile for.
3. Click the **Create Student Profile** button (`action_create_school_student`) in the
   header.
4. Open the **Result** tab.

## Post-Condition

- A `school_student` record is created in **Draft** status for the applicant (this
  admission's **Student** contact) and shown in **School Student** on the **Result**
  tab.
- The **Create Student Profile** button is no longer shown on this record.
- When this admission is later approved until **On Progress**, the existing student
  profile is reused; no second one is created (see `05-approve`).
- Creating the profile never changes the admission status.
