# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectRiskTable(models.Model):
    _name = 'project.risk.table'
    _description = 'Project Risk'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', required=True)
    risk_id = fields.Many2one(
        string='Risk', comodel_name='project.risk.risk')
    risk = fields.Char(string='Risk')
    probability_id = fields.Many2one(
        string='Probability', comodel_name='project.risk.probability.value')
    impact_id = fields.Many2one(
        string='Impact', comodel_name='project.risk.impact.value')
    risk_level = fields.Float(string='Risk Level', store=True,
                              compute='_compute_risk_level')
    action_id = fields.Many2one(
        string='Action', comodel_name='project.risk.action')
    action = fields.Char(string='Action')
    responsible_id = fields.Many2one(
        string='Responsible', comodel_name='res.users')
    causes = fields.Text(string='Causes of Risk')
    consec = fields.Text(string='Consequences')
    date_due = fields.Date(string='Term')
    level_surpassed = fields.Boolean(compute='_compute_level_surpassed')

    @api.depends('probability_id', 'probability_id.rating',
                 'impact_id', 'impact_id.rating')
    def _compute_risk_level(self):
        for record in self:
            record.risk_level = (
                record.probability_id.rating * record.impact_id.rating)

    @api.onchange('risk_id')
    def onchange_risk_id(self):
        self.risk = self.risk_id.description

    @api.onchange('action_id')
    def onchange_action_id(self):
        self.action = self.action_id.description

    @api.depends('risk_level')
    def _compute_level_surpassed(self):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        risk_limit = float(
            get_param('project_risk.risk_limit', '0.0'))
        for record in self:
            record.level_surpassed = (
                record.risk_level > risk_limit if risk_limit else False)
