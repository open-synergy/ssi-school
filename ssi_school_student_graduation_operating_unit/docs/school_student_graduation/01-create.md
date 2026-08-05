# Create School Student Graduation

> **Module:** ssi_school_student_graduation_operating_unit\
> **Extends:** ssi_school_student_graduation — model `school_student_graduation`, action
> `01-create`

## Additional Fields

When this module is installed, the create form gains one field, visible only when the
_Multi Operating Unit_ feature is enabled (Settings > Operating Unit):

- **Operating Unit**: Automatically filled with the acting user's default operating
  unit. Change if needed.

## Modified — Record Visibility

- The graduation list is now filtered by operating unit (record rule): a user only sees
  graduation records belonging to operating units they are assigned to. This is not a
  Flow step.
