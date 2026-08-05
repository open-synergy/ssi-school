# Create School Student Leave

> **Module:** ssi_school_student_leave_operating_unit\
> **Extends:** ssi_school_student_leave — model `school_student_leave`, action `01-create`

## Additional Fields

When this module is installed, the create form gains one field, visible only when the
_Multi Operating Unit_ feature is enabled (Settings > Operating Unit):

- **Operating Unit**: Automatically filled with the acting user's default operating
  unit. Change if needed.

## Modified — Record Visibility

- The leave list is now filtered by operating unit (record rule): a user only sees leave
  records belonging to operating units they are assigned to. This is not a Flow step.
