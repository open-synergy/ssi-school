.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
School Student Graduation
=========================

Records a student's graduation from school as a formal, auditable
transaction:

* **Student Graduation** -- a per-student document with a Draft ->
  Confirm -> Approve -> Done workflow. On Done, the student is set to
  the Graduated state and, if the student has an active enrollment,
  that enrollment's academic year result is set to Graduate.
* **Graduation Batch** -- a batch document that generates and drives a
  Student Graduation record for each eligible student in a cohort
  (matching Academic Year / Academic Term / Grade and having no Next
  Grade, i.e. at their final grade), reusing every per-student guard
  and side effect from the individual document.


Work Instruction
================

Student Graduation
-------------------

* `Create Student Graduation <docs/school_student_graduation/01-create.html>`_
* `Edit Student Graduation <docs/school_student_graduation/02-edit.html>`_
* `Delete Student Graduation <docs/school_student_graduation/03-delete.html>`_
* `Confirm Student Graduation <docs/school_student_graduation/04-confirm.html>`_
* `Approve Student Graduation <docs/school_student_graduation/05-approve.html>`_
* `Reject Student Graduation <docs/school_student_graduation/06-reject.html>`_
* `Cancel Student Graduation <docs/school_student_graduation/10-cancel.html>`_
* `Restart Student Graduation <docs/school_student_graduation/12-restart.html>`_
* `Reset Document Number - Student Graduation
  <docs/school_student_graduation/13-reset-number.html>`_
* `Restart Approval Process - Student Graduation
  <docs/school_student_graduation/14-restart-approval.html>`_
* `Print Student Graduation <docs/school_student_graduation/15-print.html>`_
* `Reload Template Policy - Student Graduation
  <docs/school_student_graduation/16-reload-template-policy.html>`_

Graduation Batch
-----------------

* `Create Graduation Batch <docs/school_student_graduation_batch/01-create.html>`_
* `Edit Graduation Batch <docs/school_student_graduation_batch/02-edit.html>`_
* `Delete Graduation Batch <docs/school_student_graduation_batch/03-delete.html>`_
* `Confirm Graduation Batch <docs/school_student_graduation_batch/04-confirm.html>`_
* `Approve Graduation Batch <docs/school_student_graduation_batch/05-approve.html>`_
* `Reject Graduation Batch <docs/school_student_graduation_batch/06-reject.html>`_
* `Cancel Graduation Batch <docs/school_student_graduation_batch/10-cancel.html>`_
* `Restart Graduation Batch <docs/school_student_graduation_batch/12-restart.html>`_
* `Reset Document Number - Graduation Batch
  <docs/school_student_graduation_batch/13-reset-number.html>`_
* `Restart Approval Process - Graduation Batch
  <docs/school_student_graduation_batch/14-restart-approval.html>`_
* `Print Graduation Batch <docs/school_student_graduation_batch/15-print.html>`_
* `Reload Template Policy - Graduation Batch
  <docs/school_student_graduation_batch/16-reload-template-policy.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-school
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *School Student Graduation*
6.  Install the module


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-school/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
