# Fill Random — Homeroom

> **Module:** ssi*school\
> **Model:** `school_homeroom`\
> **Menu:** School > Student Activities > Homerooms\
> **Actor:** user in group \_Homeroom — User*\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft** or **On Progress**.
- **Record:** Remaining seats are available (**Capacity** minus current **Candidate
  Students** and **Enrolled Count** is greater than zero).
- **Record:** At least one eligible student (matching the selected Grade/Term) is not
  already a Candidate or already enrolled under this batch.
- **Config:** An active `policy.template` for this model grants `fill_random_ok` for
  that state to the actor's group.
- **Access:** User is in group _Homeroom — User_.

## Flow

1. Open the **School > Student Activities > Homerooms** menu.
2. Open the record to fill.
3. On the **Generate Enrollments** tab, click the **Fill Random** button
   (`action_fill_random`).

## Post-Condition

- **Candidate Students** is filled with a random selection of eligible students, up to
  the number of remaining seats. If no seats remain or no eligible students are
  available, the list is left unchanged.
- Status does not change.
