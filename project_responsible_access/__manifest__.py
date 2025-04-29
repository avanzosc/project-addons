{
    'name': 'Project Responsible Access Control',
    'version': '16.0.1.0.0',
    'depends': ['project', 'hr_timesheet'],
    'author': 'Tu Nombre',
    'category': 'Project',
    'summary': 'Restricciones para responsables de proyectos',
    'data': [
        'security/project_groups.xml',
        'security/project_rules.xml',
        'views/project_project_view.xml',
    ],
    'installable': True,
    'application': False,
}