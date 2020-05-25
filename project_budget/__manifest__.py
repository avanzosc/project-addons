# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Project Bugdet",
    "version": "12.0.1.0.0",
    "category": "Project",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "account_budget_oca",
        "account_budget_template",
        "project",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/project_budget_groups.xml",
        "data/project_budget_data.xml",
        "views/crossovered_budget_view.xml",
        "views/crossovered_budget_line_view.xml",
        "views/project_project_view.xml",
        "views/account_analytic_account_view.xml",
        "views/res_config_settings_view.xml",
        "wizards/project_budget_search_view.xml",
        "wizards/project_initial_budget_view.xml",
    ],
    "installable": True,
}
