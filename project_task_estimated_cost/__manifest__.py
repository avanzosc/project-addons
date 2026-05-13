# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Project Task Estimated Cost",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/project-addons",
    "category": "Services/Project",
    "depends": [
        "project",
        "sale",
        "sale_project",
        "sale_project_usability",
    ],
    "data": [
        "views/project_task_views.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_install_put_product_standard_price_in_tasks",
}
