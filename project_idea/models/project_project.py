# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    author_id = fields.Many2one(
        string='Author', comodel_name='res.users')
    idea_date = fields.Date(string='Date')
    internal_idea_goal = fields.Char(string='Internal Goal')
    customer_idea_goal = fields.Char(string="Customer's Goal")
    technical_approach = fields.Text(string='Technical Approach')
    idea_type = fields.Selection(
        selection=[('training', 'Training'),
                   ('transference', 'Transference'),
                   ('internal', 'Internal'),
                   ('other', 'Other')], string='Type')
    idea_origin = fields.Selection(
        selection=[('internal', 'Internal'),
                   ('customer', 'Customer')], string='Origin')
    financing = fields.Selection(
        selection=[('industrial', 'Industrial'),
                   ('institutional', 'Institutional'),
                   ('internal', 'Internal')], string='Financing Source')
    potential_customers = fields.Char(string='Potential Customers')
    spec_line_ids = fields.Many2many(
        string='Specialization Lines', comodel_name='hr.department',
        relation='rel_project_department', column1='project_id',
        column2='department_id', domain="[('randd','=',True)]")
    human_resources_ids = fields.One2many(
        string='Human Resources', comodel_name='project.idea.resource.human',
        inverse_name='project_id')
    material_resources_ids = fields.One2many(
        string='Material Resources',
        comodel_name='project.idea.resource.material',
        inverse_name='project_id')
    cat_viability_ids = fields.One2many(
        string='Viability by Category',
        comodel_name='project.idea.cat.viability',
        inverse_name='project_id')
