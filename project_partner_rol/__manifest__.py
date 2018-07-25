# Copyright 2018 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Project Partner Rol",
    "version": "11.0.2.0.0",
    "license": "AGPL-3",
    "author":  "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Project",
    "depends": [
        "project",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/project_security.xml",
        "views/project_participant_view.xml",
        "views/project_project_view.xml",
        "views/project_participant_rol_view.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
