# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectObjetive(models.Model):
    _name = 'project.goal'
    _description = 'Goals of Projects'
    _order = 'project_id,sequence'

    project_id = fields.Many2one(
        name='Project', comodel_name='project.project', required=True,
        ondelete='cascade')
    sequence = fields.Integer(string='Sequence')
    goal_id = fields.Many2one(
        string='Goal', comodel_name='project.goal.goal',
        domain="['|',('type_id','=',type_id),('type_id','=',False)]")
    name = fields.Text(string='Goal')
    type_id = fields.Many2one(
        string='Type', comodel_name='project.goal.type', required=True)
    acceptance_range = fields.Text(string='Acceptance range')
    compliance = fields.Char(string='Compliance Degree')
    remark = fields.Char(string='Remarks')
    active = fields.Boolean(string='Active', default=True)

    @api.onchange('goal_id')
    def onchange_goal_id(self):
        self.name = self.goal_id.description

    @api.onchange('type_id')
    def onchange_type_id(self):
        if self.goal_id.type_id.id not in (self.type_id.id, False):
            self.goal_id = False
