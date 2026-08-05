# Create Enrollment Payment Template

> **Module:** ssi_school\
> **Model:** `school_enrollment_payment_template`\
> **Menu:** School > Configuration > Enrollment > Payment Templates\
> **Actor:** user in group `Enrollment Payment Template`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** At least one **Customer Invoice Type** already exists.
- **Access:** User is in group `Enrollment Payment Template`.

## Flow

1. Open the **School > Configuration > Enrollment > Payment Templates** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the payment template.
   - **Code** _(required)_: Enter a unique code identifying this template, or enter
     **/** to assign it later using **Generate Code**.
   - **Academic Term**: Select the academic term this template applies to. Leave empty
     if applicable to all terms. Optional.
   - **School**: Select the school this template applies to. Leave empty if applicable
     to all schools. Optional.
   - **Grade**: Select the specific grade level targeted by this template. Automatically
     reset to empty whenever **School** is changed. Optional.
   - **Default**: Check this box if this template must be used automatically when a
     Homeroom generates enrollments matching its Academic Term/School/Grade scope.
     Optional.
4. On the **Payment Terms** tab, add one or more payment periods. Repeat as many times
   as needed:
   - Click **Add a line**.
   - Fill in **Name**, **Sequence**, **Invoice Due Duration**, and **Due Date
     Duration**.
   - On the **Detail** tab of the term, add one or more fee lines. Repeat as many times
     as needed:
     - Click **Add a line**.
     - Fill in **Product**, **Name**, **Account**, **Quantity**, **Unit of Measure**,
       **Price**, and **Taxes**. The **Product** selection is restricted to the products
       allowed by the **Product Configuration** tab below.
5. On the **Product Configuration** tab:
   - **Product Selection Method**: Automatically defaulted to **Domain**. Change to
     **Manual** or **Python Code** if needed.
   - **Products**: Manually pick the allowed products. Shown only when **Product
     Selection Method** is **Manual**.
   - **Product Domain**: Enter the search domain used to determine allowed products.
     Shown only when **Product Selection Method** is **Domain**.
   - **Product Python Code**: Enter Python code that sets `result` to the allowed
     product recordset. Shown only when **Product Selection Method** is **Python Code**.
6. On the **Accounting** tab:
   - **Receivable Journal**: Default receivable journal copied into the enrollment.
     Optional.
   - **Receivable Account**: Default receivable account copied into the enrollment.
     Optional.
   - **Customer Invoice Type** _(required)_: Select the customer invoice type used for
     every customer invoice generated from this template's payment terms.
   - **Auto Confirm Customer Invoice**: Check this box to immediately confirm the
     generated customer invoice instead of leaving it in draft. Optional.
7. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school_enrollment_payment_template`. This
   requires an active `sequence.template` for this model — without one, the action fails
   with an error. You may also leave the Code field as **/** or type a code manually
   instead.
8. Click **Save**.

## Post-Condition

- A new Enrollment Payment Template record is created and active.
- The new template becomes eligible for automatic selection by matching Homerooms (when
  **Default** is checked), or for manual selection on an Enrollment.
