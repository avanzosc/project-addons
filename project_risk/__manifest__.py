# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Project Risk",
    "version": "11.0.4.0.0",
    "license": "AGPL-3",
    "depends": [
        "project",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Project",
    "data": [
        "security/ir.model.access.csv",
        "views/project_risk_risk_view.xml",
        "views/project_risk_action_view.xml",
        "views/project_risk_impact_value_view.xml",
        "views/project_risk_probability_value_view.xml",
        "views/project_opportunity_opportunity_view.xml",
        "views/project_opportunity_action_view.xml",
        "views/project_opportunity_impact_value_view.xml",
        "views/project_opportunity_probability_value_view.xml",
        "views/project_risk_table_view.xml",
        "views/project_opportunity_table_view.xml",
        "views/project_project_risk_view.xml",
        "views/res_config_settings_view.xml",
        "data/project_risk_data.xml",
    ],
    "installable": True,
}
