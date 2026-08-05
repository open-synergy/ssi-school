# Finish Admission Test

> **Module:** ssi*school_admission\
> **Model:** `school_admission_test`\
> **Menu:** School > Admission > Tests\
> **Actor:** user in group \_Admission Test — User*\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Config:** An active `policy.template` grants `done_ok` for state `open` to the
  actor's group.
- **Access:** User is in group _Admission Test — User_.

## Flow

1. Open the **School > Admission > Tests** menu.
2. Open the record to finish.
3. On the **Test Result** tab, check or uncheck **Passed** to record the test outcome.
   This field is only editable while the record is **On Progress**. It determines
   whether **Create School Admission** becomes available afterward — see
   `15-create-school-admission`.
4. Click the **Done** button.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
