import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-school",
    description="Meta package for open-synergy-ssi-school Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_school',
        'odoo14-addon-ssi_school_admission',
        'odoo14-addon-ssi_school_admission_customer_invoice_export',
        'odoo14-addon-ssi_school_admission_customer_invoice_export_operating_unit',
        'odoo14-addon-ssi_school_admission_lead',
        'odoo14-addon-ssi_school_admission_lead_operating_unit',
        'odoo14-addon-ssi_school_admission_operating_unit',
        'odoo14-addon-ssi_school_admission_promotion',
        'odoo14-addon-ssi_school_customer_invoice_export',
        'odoo14-addon-ssi_school_customer_invoice_export_operating_unit',
        'odoo14-addon-ssi_school_health',
        'odoo14-addon-ssi_school_incident',
        'odoo14-addon-ssi_school_incident_operating_unit',
        'odoo14-addon-ssi_school_lead',
        'odoo14-addon-ssi_school_operating_unit',
        'odoo14-addon-ssi_school_promotion',
        'odoo14-addon-ssi_school_qr_code',
        'odoo14-addon-ssi_school_student_graduation',
        'odoo14-addon-ssi_school_student_graduation_operating_unit',
        'odoo14-addon-ssi_school_student_leave',
        'odoo14-addon-ssi_school_student_leave_operating_unit',
        'odoo14-addon-ssi_school_student_withdrawal',
        'odoo14-addon-ssi_school_student_withdrawal_operating_unit',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
