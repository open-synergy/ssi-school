# Create School Admission Form

> **Module:** ssi_school_admission_operating_unit\
> **Extends:** ssi_school_admission — model `school_admission_form`, action `01-create`

## Modified — Record Visibility

- The admission form list is now filtered by operating unit (record rule): a user only
  sees admission forms belonging to operating units they are assigned to (group
  _Operating Unit_ under _School Admission Form_'s data ownership category). This is not
  a Flow step.
- **Operating Unit** is not a field the user fills directly. It is derived automatically
  from the selected **School**'s own operating unit whenever the school has exactly one.
  When the school has more than one operating unit (or none), the field is left as-is
  and can be set manually — it is visible on the form only when the _Multi Operating
  Unit_ feature is enabled (Settings > Operating Unit).
