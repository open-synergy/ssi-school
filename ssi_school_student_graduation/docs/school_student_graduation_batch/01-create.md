# Create Graduation Batch

> **Module:** ssi*school_student_graduation\
> **Model:** `school_student_graduation_batch`\
> **Menu:** School > Student Activities > Graduation Batches\
> **Actor:** user in group \_School Student Graduation Batch — User*\
> **State:** `—` → `draft`\
> **Inline Actions:** `action_populate_lines` (Populate Eligible Students)

## Pre-Condition

- **Data:** At least one student is currently **Enrolled** and at their final grade (no
  **Next Grade** set on the enrollment), so at least one line can be found when
  populating.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (needed later by `04-confirm`).
- **Access:** User is in group _School Student Graduation Batch — User_.

## Flow

1. Open the **School > Student Activities > Graduation Batches** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Date**: Defaults to today's date. Also used as the **Date** and **Graduation
     Date** of every Student Graduation document this batch generates. Change if needed.
   - **Academic Year**: Optional filter. When set, only students whose active enrollment
     belongs to this academic year are proposed when populating lines.
   - **Academic Term**: Optional filter. When set, only students whose active enrollment
     belongs to this academic term are proposed when populating lines.
   - **Grade**: Optional filter. When set, only students whose active enrollment belongs
     to this grade are proposed when populating lines.
4. On the **Students** tab, click **Populate Eligible Students** to fill the **Lines**
   list with every student currently **Enrolled**, at their final grade, and matching
   the **Academic Year** / **Academic Term** / **Grade** filters above (any filter left
   empty is not applied). This replaces the current lines. You may also add or remove
   student lines manually instead of, or after, populating. At least one line must
   remain — completing this batch will fail without one.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
