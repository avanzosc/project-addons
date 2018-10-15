# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectRiskChanceTable(models.Model):
    _name = 'project.risk.chance.table'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', required=True)
    chance = fields.Char(string='Chance')
    chance_id = fields.Many2one(
        string='Chance', comodel_name='project.risk.chance.project')
    probability_id = fields.Many2one(
        string='Probability', comodel_name='project.risk.chance.prob')
    profit_id = fields.Many2one(
        string='Profit', comodel_name='project.risk.chance.profit')
    chance_level = fields.Float(string='Chance Level', store=True,
                                compute='_compute_chance_level')
    action = fields.Char(string='Action')
    action_id = fields.Many2one(
        string='Action', comodel_name='project.risk.action')
    responsible_id = fields.Many2one(
        string='Responsible', comodel_name='res.users')
    date_due = fields.Date(string='Term')

    @api.onchange('chance_id')
    def onchange_chance_id(self):
        self.chance = self.chance_id.name

    @api.onchange('action_id')
    def onchange_action_id(self):
        self.action = self.action_id.name

    @api.depends('probability_id', 'probability_id.qualification',
                 'profit_id', 'profit_id.qualification')
    def _compute_chance_level(self):
        for record in self:
            record.chance_level = (
                record.probability_id.qualification *
                record.profit_id.qualification)
