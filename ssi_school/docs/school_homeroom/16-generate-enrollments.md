# Generate Enrollments — Homeroom

> **Module:** ssi*school\
> **Model:** `school_homeroom`\
> **Menu:** School > Student Activities > Homerooms\
> **Actor:** user in group \_Homeroom — User*\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Record:** **Candidate Students** contains at least one student that does not yet
  have an Enrollment under this batch.
- **Record:** Every Enrollment previously generated under this batch whose student is no
  longer in **Candidate Students** must already be in Draft status (otherwise it must be
  cancelled/adjusted manually first, or the student added back to **Candidate
  Students**).
- **Config:** An active `policy.template` for this model grants
  `generate_enrollments_ok` for state `open` to the actor's group.
- **Access:** User is in group _Homeroom — User_.

## Flow

1. Open the **School > Student Activities > Homerooms** menu.
2. Open the record whose enrollments will be generated.
3. On the **Generate Enrollments** tab, add or adjust **Candidate Students** if needed
   (manually or via `15-fill-random`).
4. Click the **Generate Enrollments** button (`action_generate_enrollments`).
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Any Draft Enrollment previously generated under this batch whose student is no longer
  a Candidate is deleted.
- One background job per remaining new Candidate Student is enqueued to create a Draft
  `school_enrollment` record (see `ssi_school/school_enrollment/01-create`) pre-filled
  from this batch's Academic Year, Academic Term, School, Grade, Grade Class, and
  default Payment Template. Results appear on the **Enrollments** tab as each job
  completes.
- Status does not change.
