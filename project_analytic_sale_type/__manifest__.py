# Copyright (c) 2022 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Project Analytic Sale type",
    "version": "16.0.1.0.0",
    "depends": [
        "analytic",
        "sale",
        "project",
        "sale_order_type",
    ],
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "summary": """Project Analytic Sale Type""",
    "website": "https://github.com/avanzosc/project-addons",
    "data": [
        "views/account_analytic_account_views.xml",
        "views/account_analytic_line_views.xml",
        "views/project_project_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
