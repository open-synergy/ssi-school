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
  - Fill in **Allergen**, **Severity**, and **Note**.
- **Disease History**: Record the student's disease history. Repeat as many times as
  needed:
  - Click **Add a line**.
  - Fill in **Disease**, **Date Diagnosed**, **Date Recovered**, and **Note**.

All five histories are related to the student's linked Contact and are shared with any
other student record pointing to the same Contact; every line added here is written back
to the Contact, which remains the single source of truth.

## Additional Post-Condition

- **Height (cm)**, **Weight (kg)**, and **Head Circumference (cm)** on the Health tab
  show the latest recorded value from the histories above. Read-only, computed — not
  editable directly.
