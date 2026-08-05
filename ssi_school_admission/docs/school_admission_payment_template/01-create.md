# Create Admission Payment Template

> **Module:** ssi_school_admission\
> **Model:** `school_admission_payment_template`\
> **Menu:** School > Configuration > Admission > Payment Templates\
> **Actor:** user in group `Admission Payment Template`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** At least one **Customer Invoice Type** already exists.
- **Access:** User is in group `Admission Payment Template`.

## Flow

1. Open the **School > Configuration > Admission > Payment Templates** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the payment template.
   - **Code** _(required)_: Enter a unique code identifying this template, or enter
     **/** to assign it later using **Generate Code**.
   - **Academic Term**: Select the academic term this template applies to. Optional.
   - **School**: Select the school this template applies to. Optional.
   - **Grade**: Select the grade level this template applies to. The list is filtered by
     the selected School's Grade Type. Automatically reset to empty whenever **School**
     is changed. Optional.
4. On the **Payment Terms** tab, add one or more payment periods. Repeat as many times
   as needed:
   - Click **Add a line**.
   - Fill in **Term Name**, **Sequence**, **Invoice Date Duration**, and **Due Date
     Duration**. Leave a duration field empty to skip auto-computing that term's
     corresponding estimated date on the admission record.
   - On the **Detail** tab of the term, add one or more fee lines. Repeat as many times
     as needed:
     - Click **Add a line**.
     - Fill in **Product**, **Description**, **Account**, **Quantity**, **UoM**,
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
   - **Receivable Journal**: Default receivable journal copied into the admission when
     this template is selected. Optional.
   - **Receivable Account**: Default receivable account copied into the admission when
     this template is selected. Optional.
   - **Customer Invoice Type** _(required)_: Select the customer invoice type used for
     every customer invoice generated from this template's payment terms.
   - **Auto Confirm Customer Invoice**: Check this box to immediately confirm the
     customer invoice generated from a payment term instead of leaving it in draft.
     Optional.
7. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school_admission_payment_template`. This requires
   an active `sequence.template` for this model — without one, the action fails with an
   error. You may also leave the Code field as **/** or type a code manually instead.
8. Click **Save**.

## Post-Condition

- A new Admission Payment Template record is created and active.
