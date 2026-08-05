# Create Admission Fee Template

> **Module:** ssi_school_admission\
> **Model:** `school_admission_fee_template`\
> **Menu:** School > Configuration > Admission > Fee Templates\
> **Actor:** user in group `Admission Fee Template`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group `Admission Fee Template`.

## Flow

1. Open the **School > Configuration > Admission > Fee Templates** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the fee template.
   - **Code** _(required)_: Enter a unique code identifying this template, or enter
     **/** to assign it later using **Generate Code**.
   - **School**: Select the school this template applies to. Optional.
   - **Grade**: Select the grade level this template applies to. The list is filtered by
     the selected School's Grade Type. Automatically reset to empty whenever **School**
     is changed. Optional.
   - **Journal**: Select the accounting journal used to post admission fees. Optional.
   - **Account**: Select the revenue account for recording admission fee income.
     Optional.
4. On the **Fee Lines** tab, add one or more fee lines. Repeat as many times as needed:
   - Click **Add a line**.
   - Fill in each line with:
     - **Product** _(required)_: Select the product representing the fee item.
     - **Description**: Automatically filled from **Product**. Change if needed.
     - **Account** _(required)_: Select the revenue account for posting this fee item.
     - **Quantity**: Defaults to **1**. Change if needed.
     - **UoM**: Automatically filled from **Product**. Change if needed.
     - **Price**: Enter the unit price of the fee item.
     - **Taxes**: Select the taxes applied to this fee item. Optional.
5. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school_admission_fee_template`. This requires an
   active `sequence.template` for this model — without one, the action fails with an
   error. You may also leave the Code field as **/** or type a code manually instead.
6. Click **Save**.

## Post-Condition

- A new Admission Fee Template record is created and active.
