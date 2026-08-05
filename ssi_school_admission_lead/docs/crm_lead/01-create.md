# Create CRM Lead

> **Module:** ssi_school_admission_lead\
> **Menu:** CRM > Leads\
> **Extends:** crm.lead (Odoo core CRM) — no base Instruksi Kerja exists for this model

## Additional Fields

When this module is installed, the lead/opportunity form gains the following fields:

- **Student Birthdate**: Automatically filled from **Student**'s birth date when
  **Student** is selected. Editable — changes are saved back to the **Student** contact.
- **Student Gender**: Automatically filled from **Student**'s gender when **Student** is
  selected. Editable — changes are saved back to the **Student** contact.
- **Birth City**: Automatically filled from **Student**'s city of birth when **Student**
  is selected. Editable — changes are saved back to the **Student** contact.
- **Religion**: Automatically filled from **Student**'s religion when **Student** is
  selected. Editable — changes are saved back to the **Student** contact.
- **Nationality**: Automatically filled from **Student**'s nationality when **Student**
  is selected. Editable — changes are saved back to the **Student** contact.
- **Grade**: The grade level the prospective student is applying for. The list is
  filtered by the selected **School**'s **Grade Type**. Optional at this stage; required
  later to create the admission form.
- **Previous School**: The prospective student's previous school. The list is restricted
  to the partners allowed by the company's Previous School configuration (Settings >
  School > Admission > Settings). Optional.
