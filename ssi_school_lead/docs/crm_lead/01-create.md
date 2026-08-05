# Create CRM Lead

> **Module:** ssi_school_lead\
> **Menu:** CRM > Leads\
> **Extends:** crm.lead (Odoo core CRM) — no base Instruksi Kerja exists for this model

## Additional Fields

When this module is installed, the lead/opportunity form gains the following fields:

- **School**: The school this prospective student is being routed to. Optional at this
  stage; pre-fills the **School** field on the **Create Admission** wizard.
- **Student**: The prospective student, a contact (person, not a company). Optional at
  this stage; required later to create the admission.
- **Parent Relationship**: Relationship of the **Contact** (relabeled "Parent/Guardian"
  by this module) to **Student** — Father, Mother, or Guardian. Used to link the student
  as a child/ward of the contact.
- **Student Nickname**: Automatically filled from **Student**'s nickname when
  **Student** is selected. Editable — changes are saved back to the **Student** contact.
- **Student NISN**: Automatically filled from **Student**'s National Student Number
  (NISN) record when **Student** is selected. Editable — changes are saved back to the
  **Student** contact. Only usable once **Student** is selected.
- **Parent Address** (Street, Street 2, City, State, Zip, Country): Mirrors the address
  of the **Contact** ("Parent/Guardian"). Editable — changes update the contact's
  address directly.
- **Parent Phone**, **Parent Mobile**, **Parent Email**: Mirror the corresponding field
  of the **Contact** ("Parent/Guardian"). Editable — changes update the contact
  directly.
