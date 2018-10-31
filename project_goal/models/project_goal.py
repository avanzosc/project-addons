# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectObjetive(models.Model):
    _name = 'project.goal'
    _description = 'Goals of Projects'

    project_id = fields.Many2one(comodel_name='project.project')
    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Name')
    type_id = fields.Many2one(
        string='Type', comodel_name='project.goal.type')
    acceptance_range = fields.Text(string='Acceptance range')
    compliance = fields.Char(string='Compliance Degree')
    remark = fields.Char(string='Remarks')
