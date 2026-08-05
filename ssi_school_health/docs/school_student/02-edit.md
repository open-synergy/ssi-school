# Edit Student

> **Module:** ssi_school_health\
> **Extends:** ssi_school — model `school_student`, aksi `02-edit`

## Additional Fields

The **Health** tab described in `01-create` remains available for editing:

- **Heights**, **Weights**, **Head Circumferences**: Add, edit, or remove history lines
  as needed.
- **Allergies**: Add, edit, or remove lines as needed.
- **Disease History**: Add, edit, or remove lines as needed.

## Additional Post-Condition

- **Height (cm)**, **Weight (kg)**, and **Head Circumference (cm)** are recomputed from
  the latest history line whenever a line is added, edited, or removed.
