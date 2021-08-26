# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Project Task Framework",
    'version': '13.0.1.0.0',
    "author": "Avanzosc",
    "category": "Project",
    "depends": [
        "project",
        "hr_timesheet",
        "account",
        "project_category",
        "project_timeline",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project_task_views.xml",
        "views/project_task_framework_views.xml",
        "views/account_analytic_line_views.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
