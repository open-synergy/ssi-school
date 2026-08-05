.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

======================
School Admission Lead
======================

Glue module between School Admission and CRM Lead.

Adds ``admission_form_id`` and ``admission_test_id`` fields to ``crm.lead``,
and provides a wizard to create an admission form directly from a lead.

It also carries the first layer of admission intake data on the lead itself:

* ``student_birthdate`` and ``student_gender``: birthdate and gender of the
  prospective student, related to the contact referenced by ``student_id``.
  The identity data is stored on ``res.partner``, not duplicated on the lead.
* ``birth_city``, ``religion_id`` and ``nationality_id``: place of birth,
  religion and nationality of the prospective student, related to the
  contact referenced by ``student_id``. The identity data is stored on
  ``res.partner``, not duplicated on the lead.
* ``grade_id``: the grade level the prospective student applies for, restricted
  by ``grade_type_id`` which is derived from the selected school.
* ``previous_school_id``: the prospective student's previous school, a
  ``res.partner`` reference restricted to ``allowed_previous_school_ids``.
  The list of partners that can be selected is configurable per company
  (``previous_school_selection_method``: manual/domain/code) from
  **Settings > School > Admission > Settings**, without a code release.

Work Instruction
=================

CRM Lead
--------

* `Create CRM Lead <docs/crm_lead/01-create.html>`_
* `Create Admission Form from CRM Lead <docs/crm_lead/02-create-admission-form.html>`_
* `Open Admission Test from CRM Lead <docs/crm_lead/03-open-admission-test.html>`_

Credits
=======

Contributors
------------

* PT. Simetri Sinergi Indonesia
* OpenSynergy Indonesia
