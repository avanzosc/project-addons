.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

====================
Project Task Meeting
====================

Overview
========

The **Project Task Meeting** module enhances the Odoo project management system by linking project tasks with calendar events. It provides a seamless connection between tasks and their related meetings, allowing users to efficiently manage and track their project activities.

Features
========

- **Link Tasks to Calendar Events**:
  - Adds a Many2one field in calendar events to reference the related project task.
  - Displays the task's customer information in the calendar event form.

- **Task-Related Meeting Count**:
  - Shows the count of related calendar events directly on the project task form and list views.

- **Navigation Shortcut**:
  - Adds a button in the project task form to quickly navigate to related calendar events.

- **Enhanced Calendar Views**:

  - **Calendar Event Views**:
    - Adds task-related fields to calendar event forms, tree views, and search views.
  - **Project Task Views**:
    - Includes a field to display the number of related calendar events in task forms and tree views.

Usage
=====

After installing the module, you will see:

- **Calendar Events**:
  - A new field to link each calendar event to a project task.
  - The task's customer information will be displayed in the calendar event form.

- **Project Tasks**:
  - A new field to display the count of related calendar events.
  - A button labeled "Meetings" to open the related calendar events directly from the project task form.


Testing
=======

The module includes automated tests to ensure functionality:

- **TestProjectTaskEvent**:
  - Verifies that the count of calendar events is correctly displayed.
  - Checks that the navigation to calendar events from a task works as expected.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/project-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
~~~~~~~~~~~~

* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente<alfredodelafuente@avanzosc.es>

