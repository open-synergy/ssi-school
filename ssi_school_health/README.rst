.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============
School Health
=============


This module exposes the health data recorded on a contact (``res.partner``) by
``ssi_partner_health`` directly on the ``school_student`` form, through a new
*Health* page.

School staff can read and maintain the student's anthropometric measurement
history (height, weight, head circumference), allergies, and disease history
without leaving the student form. No health data is duplicated: every field is
related to the student's contact, which remains the single source of truth.


Work Instruction
=================

Student
-------

* `Create Student <docs/school_student/01-create.html>`_
* `Edit Student <docs/school_student/02-edit.html>`_

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-school
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *School Health*
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
