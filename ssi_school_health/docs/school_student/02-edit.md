# Edit Student

> **Module:** ssi_school_health\
> **Extends:** ssi_school — model `school_student`, aksi `02-edit`

## Additional Fields

The **Health** tab described in `01-create` remains available for editing:

- **Heights**, **Weights**, **Head Circumferences**: Add, edit, or remove history lines
  as needed.
- **Allergies**: Add, edit, or remove lines as needed.
- **Disease History**: Add, edit, or remove lines as needed.
- **Medications**: Add, edit, or remove lines as needed.
- **Health Providers**: Add, edit, or remove lines as needed. Drag a line's handle to
  change its **Sequence**.

## Additional Post-Condition

- **Height (cm)**, **Weight (kg)**, and **Head Circumference (cm)** are recomputed from
  the latest history line whenever a line is added, edited, or removed.
- **Family Doctor** and **Health Facility** are recomputed whenever a Health Providers
  line is added, edited, removed, or reordered.
