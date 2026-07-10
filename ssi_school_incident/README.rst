.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============
School Incident
===============

Student incident and parent complaint handling, implementing the YPII
Incident & Parent Complaint Handling Guideline (v2.0):

* **Master Log incident tracking with SLA/escalation** -- log incident and
  parent complaint cases (School Incident) against configurable Incident
  Types, track first-contact and resolution SLAs per handling tier, keep a
  full parent contact history, and escalate a case to a higher handling
  tier against explicit, auditable Escalation Criteria.
* **Three-Color Academic Warning System** -- evaluate a student's academic
  standing (School Academic Alert) against configurable Academic Alert
  Levels (Yellow/Orange/Red), and create a linked School Incident once an
  Orange or Red alert is confirmed.
* **Weekly Case Review** -- a lightweight, checklist-driven Weekly Case
  Review that collects the period's School Incident cases and audits SLA
  breaches, unresolved cases, and escalation-criteria compliance.


Work Instruction
=================

Incident Type
-------------

* `Create Incident Type <docs/school_incident_type/01-create.html>`_
* `Edit Incident Type <docs/school_incident_type/02-edit.html>`_
* `Delete Incident Type <docs/school_incident_type/03-delete.html>`_
* `Deactivate Incident Type <docs/school_incident_type/04-deactivate.html>`_
* `Activate Incident Type <docs/school_incident_type/05-activate.html>`_

Incident Escalation Criteria
-----------------------------

* `Create Incident Escalation Criteria <docs/school_incident_escalation_criteria/01-create.html>`_
* `Edit Incident Escalation Criteria <docs/school_incident_escalation_criteria/02-edit.html>`_
* `Delete Incident Escalation Criteria <docs/school_incident_escalation_criteria/03-delete.html>`_
* `Deactivate Incident Escalation Criteria <docs/school_incident_escalation_criteria/04-deactivate.html>`_
* `Activate Incident Escalation Criteria <docs/school_incident_escalation_criteria/05-activate.html>`_

Academic Alert Level
---------------------

* `Create Academic Alert Level <docs/school_academic_alert_level/01-create.html>`_
* `Edit Academic Alert Level <docs/school_academic_alert_level/02-edit.html>`_
* `Delete Academic Alert Level <docs/school_academic_alert_level/03-delete.html>`_
* `Deactivate Academic Alert Level <docs/school_academic_alert_level/04-deactivate.html>`_
* `Activate Academic Alert Level <docs/school_academic_alert_level/05-activate.html>`_

School Incident
----------------

* `Create School Incident <docs/school_incident/01-create.html>`_
* `Edit School Incident <docs/school_incident/02-edit.html>`_
* `Delete School Incident <docs/school_incident/03-delete.html>`_
* `Confirm School Incident <docs/school_incident/04-confirm.html>`_
* `Approve School Incident <docs/school_incident/05-approve.html>`_
* `Reject School Incident <docs/school_incident/06-reject.html>`_
* `Finish School Incident <docs/school_incident/09-finish.html>`_
* `Cancel School Incident <docs/school_incident/10-cancel.html>`_
* `Restart School Incident <docs/school_incident/12-restart.html>`_
* `Reset Document Number - School Incident <docs/school_incident/13-reset-document-number.html>`_
* `Escalate School Incident <docs/school_incident/14-escalate.html>`_

School Academic Alert
-----------------------

* `Create School Academic Alert <docs/school_academic_alert/01-create.html>`_
* `Edit School Academic Alert <docs/school_academic_alert/02-edit.html>`_
* `Delete School Academic Alert <docs/school_academic_alert/03-delete.html>`_
* `Confirm School Academic Alert <docs/school_academic_alert/04-confirm.html>`_
* `Approve School Academic Alert <docs/school_academic_alert/05-approve.html>`_
* `Reject School Academic Alert <docs/school_academic_alert/06-reject.html>`_
* `Finish School Academic Alert <docs/school_academic_alert/09-finish.html>`_
* `Cancel School Academic Alert <docs/school_academic_alert/10-cancel.html>`_
* `Restart School Academic Alert <docs/school_academic_alert/12-restart.html>`_
* `Reset Document Number - School Academic Alert <docs/school_academic_alert/13-reset-document-number.html>`_
* `Evaluate School Academic Alert <docs/school_academic_alert/14-evaluate.html>`_
* `Create Incident from School Academic Alert <docs/school_academic_alert/15-create-incident.html>`_

School Incident Weekly Review
-------------------------------

* `Create School Incident Weekly Review <docs/school_incident_weekly_review/01-create.html>`_
* `Edit School Incident Weekly Review <docs/school_incident_weekly_review/02-edit.html>`_
* `Delete School Incident Weekly Review <docs/school_incident_weekly_review/03-delete.html>`_
* `Confirm School Incident Weekly Review <docs/school_incident_weekly_review/04-confirm.html>`_
* `Approve School Incident Weekly Review <docs/school_incident_weekly_review/05-approve.html>`_
* `Reject School Incident Weekly Review <docs/school_incident_weekly_review/06-reject.html>`_
* `Cancel School Incident Weekly Review <docs/school_incident_weekly_review/10-cancel.html>`_
* `Restart School Incident Weekly Review <docs/school_incident_weekly_review/12-restart.html>`_
* `Reset Document Number - School Incident Weekly Review <docs/school_incident_weekly_review/13-reset-document-number.html>`_
* `Collect Incidents into School Incident Weekly Review <docs/school_incident_weekly_review/14-collect-incidents.html>`_
* `Fill in the Weekly Case Review Checklist <docs/school_incident_weekly_review/15-checklist.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-school
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *School Incident*
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
