# Return Student Leave

> **Module:** ssi*school_student_leave\
> **Model:** `school_student_leave`\
> **Menu:** School > Student Activities > Student Leaves\
> **Actor:** user in group \_School Student Leave — Viewer*\
> **Requires:** `05-approve`

This IK documents the `action_return` button.

## Pre-Condition

- **Record:** Status is **Done**.
- **Record:** The student is currently in the **On Leave** state
  (`school_student.state = "on_leave"`). Attempting this action when the student is not
  on leave raises an error.
- **Access:** User is in group _School Student Leave — Viewer_ (the minimum group with
  access to the menu). The **Return** button carries no additional group or policy
  restriction — it is gated only by the record's status.

## Flow

1. Open the **School > Student Activities > Student Leaves** menu.
2. Open the record whose status is **Done** and whose student is currently **On Leave**.
3. Click the **Return** button.

## Post-Condition

- The linked student's status changes from **On Leave** to **Enrolled**
  (`school_student.state` = `"enrol"`, via `action_set_to_enroll()`).
- This leave document's own status is **not** changed by this action — it remains
  **Done**. The leave document itself is not reverted through the workflow; only the
  student's status is updated.
- The student's active enrollment record (`school_enrollment`) is not modified by this
  action.

> **Note:** Unlike `04-confirm` / `05-approve` / `06-reject` / `10-cancel` /
> `12-restart` / `14-restart-approval`, clicking **Return** does **not** show a
> confirmation dialog — the button has no `confirm` attribute in the view.
