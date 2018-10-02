# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectRiskTable(models.Model):
    _name = 'project.risk.table'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project')
    risk_id = fields.Many2one(
        string='Risk', comodel_name='project.risk.risk')
    probability_id = fields.Many2one(
        string='Probability', comodel_name='project.risk.probability.value')
    impact_id = fields.Many2one(
        string='Impact', comodel_name='project.risk.impact.value')
    risk_level = fields.Float(string='Risk Level')
    action_id = fields.Many2one(
        string='Action', comodel_name='project.risk.action')
    manager = fields.Char(string='Manager')
    term = fields.Float(string='Term')
    tracing = fields.Text(string='Tracing')
