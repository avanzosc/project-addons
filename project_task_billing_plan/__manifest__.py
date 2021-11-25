# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Project Task Billing Plan",
    "version": "11.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "account_analytic_billing_plan",
        "account_invoice_task",
        "project_billing_plan",
    ],
    "excludes": [],
    "data": [
        "views/account_analytic_billing_plan_view.xml",
        "views/project_task_view.xml",
    ],
    "installable": True,
}
