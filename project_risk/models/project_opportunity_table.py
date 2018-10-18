# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectOpportunityTable(models.Model):
    _name = 'project.opportunity.table'
    _description = 'Project Opportunity'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', required=True)
    opportunity = fields.Char(string='Opportunity')
    opportunity_id = fields.Many2one(
        string='Chance', comodel_name='project.opportunity.opportunity')
    probability_id = fields.Many2one(
        string='Probability',
        comodel_name='project.opportunity.probability.value')
    impact_id = fields.Many2one(
        string='Profit', comodel_name='project.opportunity.impact.value')
    chance_level = fields.Float(string='Chance Level', store=True,
                                compute='_compute_chance_level')
    action = fields.Char(string='Action')
    action_id = fields.Many2one(
        string='Action', comodel_name='project.opportunity.action')
    responsible_id = fields.Many2one(
        string='Responsible', comodel_name='res.users')
    date_due = fields.Date(string='Term')

    @api.onchange('opportunity_id')
    def onchange_opportunity_id(self):
        self.opportunity = self.opportunity_id.name

    @api.onchange('action_id')
    def onchange_action_id(self):
        self.action = self.action_id.name

    @api.depends('probability_id', 'probability_id.rating',
                 'impact_id', 'impact_id.rating')
    def _compute_chance_level(self):
        for record in self:
            record.chance_level = (
                record.probability_id.rating *
                record.impact_id.rating)
