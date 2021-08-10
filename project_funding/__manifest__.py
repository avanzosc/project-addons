# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Project Funding",
    "version": "11.0.3.0.0",
    "license": "AGPL-3",
    "depends": [
        "project",
        "partner_funding_source",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Project",
    "data": [
        "security/project_funding_security.xml",
        "security/ir.model.access.csv",
        "data/project_funding_data.xml",
        "views/funding_source_project_view.xml",
        "views/project_project_view.xml",
        "views/project_funding_view.xml",
        "views/res_config_settings_view.xml",
    ],
    "installable": True,
}
