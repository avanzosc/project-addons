.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================
Project Task Employee
=====================

Overview
--------

Adds responsible field linking to employee in project tasks.

Features
--------

- Adds a "Responsible" field linking to an employee in project tasks.
- Integrates the field into both form and tree views with optional visibility settings.

Usage
-----

Once installed, the `project_task_employee` module will add the "Responsible" field to the Project Task form view and list view (tree view). You can link tasks to employees to designate responsibility.

Technical Details
-----------------

- The module extends the `project.task` model to include a Many2one field linking to `hr.employee`.
- Views are modified using XML templates (`project_task_views.xml`) to integrate the new field seamlessly into the Odoo user interface.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
