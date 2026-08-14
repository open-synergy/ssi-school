.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================
School + Promotion
==================

Glue module that lets a promotion code be redeemed directly against one School
Enrollment payment term. Adds ``mixin.promotion_object`` to
``school_enrollment_payment_term``, so each payment term line tracks its own
Promotion Code Usages and exposes its own invoice's receivable journal item to
``action_populate_allocation``.


Work Instruction
=================

Enrollment
----------

* `Create Enrollment <docs/school_enrollment/01-create.html>`_
* `Edit Enrollment <docs/school_enrollment/02-edit.html>`_


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
