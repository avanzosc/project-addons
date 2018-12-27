# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Project Task Cost",
    "version": "11.0.2.0.0",
    "license": "AGPL-3",
    "depends": [
        "project",
        "hr",
        "sale_timesheet",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Project",
    "data": [
        "security/project_task_cost_security.xml",
        "views/project_task_view.xml",
    ],
    "installable": True,
    "post_init_hook": "post_init_hook",
}
