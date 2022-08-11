# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Task Logs Usability in Projects",
    "version": "14.0.1.0.0",
    "category": "Services/Timesheets",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/project-addons",
    "depends": [
        "hr_timesheet",
        "project",
    ],
    "excludes": [],
    "data": [
        "security/ir.model.access.csv",
        "views/project_task_views.xml",
        # "reports/project_task_timesheet_report_views.xml",
    ],
    "installable": True,
}
