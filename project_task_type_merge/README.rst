.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=======================
Project Task Type Merge
=======================

Extension of the OCA module ``project_task_default_stage``.

* Show the task stages configuration list and kanban **ungrouped** (it removes
  the default grouping by project, so the stages are listed normally).

* **Merge** project task stages (``project.task.type``) that share the same
  name into a single one. For each group of stages with the same name it keeps
  one canonical stage (the lowest-id active stage, or the lowest-id one when
  the whole group is archived), links all the related projects to it, moves all
  its tasks to it (archived ones included) and deletes the duplicates. Personal
  stages (with a stage owner) are never touched.

  The merge runs once on install (``post_init_hook``) and can be relaunched
  manually at any time from the server action **Merge Duplicate Task Stages**,
  available in *Project > Configuration*.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/project-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* AvanzOSC

Contributors
------------

* AvanzOSC <https://www.avanzosc.es>
