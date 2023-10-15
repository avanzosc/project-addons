# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Project Analysis",
    "version": "11.0.1.0.0",
    "category": "Project",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "project",
        "hr_timesheet",
        "project_characterization",
    ],
    "data": [
        # "security/ir.model.access.csv",
        "data/employee_payroll_data.xml",
        "views/hr_employee_view.xml",
        "views/project_project_view.xml",

    ],
    "installable": True,
}
