# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectObjetive(models.Model):
    _name = 'project.goal'
    _description = 'Goals of Projects'
    _order = 'project_id,sequence'

    project_id = fields.Many2one(
        name='Project', comodel_name='project.project', required=True,
        ondelete='cascade')
    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Name')
    type_id = fields.Many2one(
        string='Type', comodel_name='project.goal.type', required=True)
    acceptance_range = fields.Text(string='Acceptance range')
    compliance = fields.Char(string='Compliance Degree')
    remark = fields.Char(string='Remarks')
    active = fields.Boolean(string='Active', default=True)
