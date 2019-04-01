# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Project Bugdet Expense",
    "version": "11.0.1.0.0",
    "category": "Project",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "account",
        "account_cancel",
        "account_budget_expense",
        "project_budget",
        "project_task_cost",
    ],
    "data": [
        "data/project_budget_expense_data.xml",
        "data/project_budget_expense_cron.xml",
        "views/crossovered_budget_view.xml",
        "views/hr_employee_view.xml",
        "wizards/hr_timesheet_to_accounting_view.xml",
    ],
    "installable": True,
}
