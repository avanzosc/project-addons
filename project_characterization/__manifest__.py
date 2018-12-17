# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Project Characterization",
    "version": "11.0.6.0.0",
    "license": "AGPL-3",
    "depends": [
        "project",
        "account",
        "base_characterization",
        "project_funding",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Project",
    "data": [
        "security/ir.model.access.csv",
        "views/account_analytic_view.xml",
        "views/project_project_view.xml",
        "views/project_task_view.xml",
        "views/project_characterization_view.xml",
        "views/res_area_view.xml",
        "views/res_config_settings_view.xml",
    ],
    "installable": True,
}
