# Create Admission Test

> **Module:** ssi*school_admission\
> **Model:** `school_admission_test`\
> **Menu:** School > Admission > Tests\
> **Actor:** user in group \_Admission Test — User*\
> **State:** `—` → `draft`\
> **Requires:** `ssi_school_admission/school_admission_form/16-create-admission-test`

## Pre-Condition

- **Config:** An active `sequence.template` exists for this model, so the test receives
  a document number once it reaches **On Progress**.
- **Data:** The **School** and **Student** records already exist.
- **Data:** (Optional) A `school_admission_form` in **Done** status, if this test
  originates from one — see
  `ssi_school_admission/school_admission_form/16-create-admission-test`. A test can also
  be created directly from this menu without an originating form.
- **Access:** User is in group _Admission Test — User_.

## Flow

1. Open the **School > Admission > Tests** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Date**: Automatically filled with today's date. Change if needed.
   - **Academic Year** _(required)_: Select the academic year.
   - **Academic Term** _(required)_: Select the academic term. The list is filtered by
     the selected **Academic Year**.
   - **School** _(required)_: Select the school.
   - **Grade** _(required)_: Select the grade level. The list is filtered by the
     school's **Grade Type**.
   - **Admission Form**: Optional. If selected, **Student** is automatically filled from
     the form. A given admission form can be linked to only one test.
   - **Student** _(required)_: Automatically filled if **Admission Form** is selected.
     Otherwise, select the student taking this test manually.
4. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
