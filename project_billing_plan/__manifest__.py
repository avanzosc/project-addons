# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Project Billing Plan",
    "version": "12.0.1.0.0",
    "category": "Project",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "account_analytic_billing_plan",
        "project",
        "hr_timesheet",
    ],
    "data": [
        "views/project_project_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
