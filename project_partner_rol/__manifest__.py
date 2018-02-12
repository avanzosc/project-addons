# -*- coding: utf-8 -*-
# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Project Partner Rol',
    'version': '11.0.1.1.0',
    'license': "AGPL-3",
    'summary': '''Project partner rol''',
    'author':  "AvanzOSC",
    'website': 'http://www.avanzosc.es',
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    'category': 'Project',
    'depends': [
        'project',
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/project_participant_view.xml",
        "views/project_project_view.xml",
        "views/project_participant_rol_view.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
