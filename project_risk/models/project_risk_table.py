# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectRiskTable(models.Model):
    _name = 'project.risk.table'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', required=True)
    risk_id = fields.Many2one(
        string='Risk', comodel_name='project.risk.risk')
    probability_id = fields.Many2one(
        string='Probability', comodel_name='project.risk.probability.value')
    impact_id = fields.Many2one(
        string='Impact', comodel_name='project.risk.impact.value')
    risk_level = fields.Float(string='Risk Level', store=True,
                              compute='_compute_risk_level')
    action_id = fields.Many2one(
        string='Action', comodel_name='project.risk.action')
    responsible_id = fields.Many2one(
        string='Responsible', comodel_name='res.users')
    term = fields.Float(string='Term')
    tracing = fields.Text(string='Tracing')
    
    @api.depends('probability_id', 'probability_id.rating',
                 'impact_id', 'impact_id.rating')
    def _compute_risk_level(self):
        for record in self:
            record.risk_level = (
                record.probability_id.rating * record.impact_id.rating)
