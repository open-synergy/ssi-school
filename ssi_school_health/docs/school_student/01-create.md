# Create Student

> **Module:** ssi_school_health\
> **Extends:** ssi_school — model `school_student`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains a **Health** tab:

- **Heights**: Record the student's height history. Repeat as many times as needed:
  - Click **Add a line**.
  - Fill in **Date** and **Value** (cm).
- **Weights**: Record the student's weight history. Repeat as many times as needed:
  - Click **Add a line**.
  - Fill in **Date** and **Value** (kg).
- **Head Circumferences**: Record the student's head circumference history. Repeat as
  many times as needed:
  - Click **Add a line**.
  - Fill in **Date** and **Value** (cm).
- **Allergies**: Record the student's allergies. Repeat as many times as needed:
  - Click **Add a line**.
  - Fill in **Allergen**, **Severity**, **Reactions**, and **Note**.
- **Disease History**: Record the student's disease history. Repeat as many times as
  needed:
  - Click **Add a line**.
  - Fill in **Disease**, **Date Diagnosed**, **Date Recovered**, and **Note**.
- **Medications**: Record medications the student is or was taking. Repeat as many times
  as needed:
  - Click **Add a line**.
  - Fill in **Medication**, **Dose**, **Frequency**, **Route**, **Start Date**, **End
    Date**, and **Instruction**.
- **Health Providers**: Record the student's health care providers (physicians and
  health facilities). Repeat as many times as needed:
  - Click **Add a line**.
  - Fill in **Provider**, **Role**, **Start Date**, and **Note**.

All seven histories are related to the student's linked Contact and are shared with any
other student record pointing to the same Contact; every line added here is written back
to the Contact, which remains the single source of truth.

## Additional Post-Condition

- **Height (cm)**, **Weight (kg)**, and **Head Circumference (cm)** on the Health tab
  show the latest recorded value from the histories above. Read-only, computed — not
  editable directly.
- **Ongoing** on a Medications line is filled in automatically: checked while **End
  Date** is empty. Read-only — not a manual checkbox.
- **Family Doctor** and **Health Facility** on the Health tab are filled in
  automatically: the top-ranked individual and organization provider (by Sequence) in
  Health Providers. Read-only, computed — change them by adding or reordering a Health
  Providers line.
