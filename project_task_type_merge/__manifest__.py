# Copyright 2026 AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Project Task Type Merge",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/project-addons",
    "category": "Services/Project",
    "depends": [
        "project_task_default_stage",
    ],
    "data": [
        "views/project_task_type_views.xml",
        "data/server_action.xml",
    ],
    "installable": True,
    "post_init_hook": "post_init_hook",
}
