# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    author_id = fields.Many2one(
        string='Author', comodel_name='res.users')
    idea_date = fields.Date(string='Date')
    internal_goal = fields.Char(string='Internal Goal')
    customer_goal = fields.Char(string="Customer's Goal")
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
