# Create Homeroom

> **Module:** ssi_school_operating_unit\
> **Extends:** ssi_school — model `school_homeroom`, action `01-create`

## Additional Fields

When this module is installed, the create form gains one field:

- **Operating Unit**: Automatically filled from the current user's default operating
  unit. Change if needed. Only visible to users in the _Multiple Operating Unit_ group.

## Additional Post-Condition

- Every Enrollment generated from this Homeroom batch (`16-generate-enrollments`) is
  created with the same **Operating Unit** as the Homeroom.

## Modified — Record Visibility

- Users in the _Operating Unit_ group only see, edit, and delete Homeroom records whose
  Operating Unit matches one of their own Operating Units. Users outside this group are
  not restricted by this rule.
