.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===========================
Project Milestone Usability
===========================

This module improves the usability of project milestones in Odoo.

**Features**

- Menu under Project → Tasks to access Milestones.
- Extends the milestone list view with billable status, completion status, task counts, missing tasks, UoM, quantities, project, customer, quantity percentage, reached date, sale line info, and deadline indicators (future/exceeded). Project and Customer columns are read-only here.
- Stored computed field "Missing Tasks" (task_count - done_task_count).
- Search view adds filters for Project, Customer, and "Has Missing Tasks" (> 0), plus group by Project and Customer.

**Quick usage**

1. Go to Project → Tasks → Milestones.
2. Use the list view columns (optional show) to review/edit milestones; project/customer stay read-only.
3. Filter by "Has Missing Tasks" to focus on pending work; group by Project or Customer as needed.

**Technical details**

- Model extension: `project.milestone` (stored computed `tasks_missing`).
- Views: inherits the milestone list and adds a search view with filters/groups.
- Action & menu: milestones action with list/form; menu under `project.menu_project_management`.
- Dependencies: `project`, `sale_management`, `sale_project`.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/project-addons/issues>`_.

Credits
=======

Authors
-------

* AvanzOSC

Contributors
------------

* Aner Arregi <aneravanzosc@gmail.com>
* Ana Juaristi <anajuaristi@avanzosc.es>

Maintainer
----------

This module is maintained by AvanzOSC.
