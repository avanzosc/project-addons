# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Project Characterization",
    "version": "11.0.2.1.0",
    "license": "AGPL-3",
    "depends": [
        "project",
        "account",
        "hr",
        "crm",
        "base_characterization",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Project",
    "data": [
        "security/ir.model.access.csv",
        "views/account_analytic_view.xml",
        "views/funding_source_view.xml",
        "views/project_project_view.xml",
        "views/project_task_view.xml",
        "views/project_characterization_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
