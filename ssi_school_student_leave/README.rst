.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================
School Student Leave
====================

Drives a student's Leave of Absence through a Draft -> Confirm ->
Approve -> Done workflow, valid for exactly one academic term. On
Done, the linked student (school_student) is transitioned to the
on_leave state. Once the leave period is over, the Return button
re-enrolls the student directly, with no separate approval step.


Work Instruction
================

Student Leave
-------------

* `Create Student Leave <docs/school_student_leave/01-create.html>`_
* `Edit Student Leave <docs/school_student_leave/02-edit.html>`_
* `Delete Student Leave <docs/school_student_leave/03-delete.html>`_
* `Confirm Student Leave <docs/school_student_leave/04-confirm.html>`_
* `Approve Student Leave <docs/school_student_leave/05-approve.html>`_
* `Reject Student Leave <docs/school_student_leave/06-reject.html>`_
* `Cancel Student Leave <docs/school_student_leave/10-cancel.html>`_
* `Restart Student Leave <docs/school_student_leave/12-restart.html>`_
* `Reset Document Number - Student Leave
  <docs/school_student_leave/13-reset-number.html>`_
* `Restart Approval Process - Student Leave
  <docs/school_student_leave/14-restart-approval.html>`_
* `Return Student Leave <docs/school_student_leave/15-return.html>`_
* `Print Student Leave <docs/school_student_leave/16-print.html>`_
* `Reload Template Policy - Student Leave
  <docs/school_student_leave/17-reload-template-policy.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-school
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *School Student Leave*
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
