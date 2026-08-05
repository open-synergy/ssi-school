# Create Admission Form from CRM Lead

> **Module:** ssi_school_admission_lead_operating_unit\
> **Extends:** ssi_school_admission_lead — model `crm.lead`, action `02-create-admission-form`

## Modified Flow

- Anchor: on the base Flow's step 4 (fill in the **Create Admission Form** wizard), the
  wizard gains one field:
  - **Operating Unit**: Pre-filled from the lead's own **Operating Unit**, if set (via
    the button's context); otherwise left empty. Change if needed.

## Additional Post-Condition

- The new `school_admission_form` document is created with its **Operating Unit** set to
  the wizard's **Operating Unit**, when one was selected.
