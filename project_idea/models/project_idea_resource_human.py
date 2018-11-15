# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class HumanResources(models.Model):
    _name = 'project.idea.resource.human'
    _description = 'Idea Human Resource'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', required=True)
    human_department_id = fields.Many2one(
        string='Department', comodel_name='hr.department')
    human_level = fields.Selection(
        selection=[('1', '1'),
                   ('2', '2'),
                   ('3', '3')], string='Level')
    human_intensity = fields.Selection(
        selection=[('high', 'High'),
                   ('medium', 'Medium'),
                   ('low', 'Low')], string='Intensity')
    active = fields.Boolean(string='Active', default=True)
