# Create School Academic Alert

> **Module:** ssi_school_incident_operating_unit\
> **Extends:** ssi_school_incident — model `school_academic_alert`, action `01-create`

## Additional Fields

When this module is installed, the create form gains one field, visible only when the
_Multi Operating Unit_ feature is enabled (Settings > Operating Unit):

- **Operating Unit**: Automatically filled with the acting user's default operating
  unit. Change if needed.

## Modified — Record Visibility

- The academic alert list is now filtered by operating unit (record rule): a user only
  sees academic alerts belonging to operating units they are assigned to. Manager
  (Principal) is also evaluated against this rule. This is not a Flow step.
