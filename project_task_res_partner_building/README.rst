.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: License: LGPL-3

=====================
Project Task Building
=====================

Overview
========

The **Project Task Building** module extends the standard Odoo **Project** application by adding a new field to associate tasks with specific buildings (represented by `res.partner` records).

Features
========

- Adds a new field **"Building"** (`building_id`) to project tasks.
- The field is displayed in the task form view, just after the **Customer** (`partner_id`) field.
- The **Building** is a Many2one relation to `res.partner`, allowing reuse of existing partner records for building identification.

Use Case
========

This is particularly useful for construction, property management, or maintenance companies where each task must be linked to a specific building.

For example:
- A maintenance request can be assigned to a task and associated with the building it belongs to.
- Projects spanning multiple buildings can track individual tasks per location.

Usage
=====

1. Go to **Project > Tasks**.
2. Open any task form.
3. You will find a new field labeled **Building** after the **Customer** field.
4. Select a partner record that represents the building related to this task.

Configuration
=============

No additional configuration is required after installation.

Bug Tracker
===========

If you find any issues or bugs, please report them at:
`https://github.com/avanzosc/project-addons/issues <https://github.com/avanzosc/project-addons/issues>`_

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

License
=======

This module is licensed under the LGPL-3 License.

See: https://www.gnu.org/licenses/lgpl-3.0.html
