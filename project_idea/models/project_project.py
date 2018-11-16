# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    idea_type = fields.Selection(
        selection=[('training', 'Training'),
                   ('transference', 'Transference'),
                   ('internal', 'Internal'),
                   ('other', 'Other')], string='Type')
    idea_origin = fields.Selection(
        selection=[('internal', 'Internal'),
                   ('customer', 'Customer')], string='Origin')
    potential_customers = fields.Char(string='Potential Customers')
    spec_line_ids = fields.Many2many(
        string='Specialization Lines', comodel_name='hr.department',
        relation='rel_project_department', column1='project_id',
        column2='department_id', domain="[('randd','=',True)]")
    human_resources_ids = fields.One2many(
        string='Human Resources', comodel_name='project.idea.resource.human',
        inverse_name='project_id', copy=True, context={'active_test': False})
    material_resources_ids = fields.One2many(
        string='Material Resources',
        comodel_name='project.idea.resource.material',
        inverse_name='project_id', copy=True, context={'active_test': False})
    year_duration = fields.Integer(string='Estimated term (years)')

    @api.multi
    def write(self, vals):
        res = super(ProjectProject, self).write(vals) if vals else True
        if 'active' in vals:
            # archiving/unarchiving a project does it on its human
            # and material resources, too
            self.with_context(active_test=False).mapped(
                'human_resources_ids').write(
                {'active': vals['active']})
            self.with_context(active_test=False).mapped(
                'material_resources_ids').write(
                {'active': vals['active']})
        return res
