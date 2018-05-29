# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    res_area_id = fields.Many2one(
        comodel_name='res.area', string='Area')
    op_space_id = fields.Many2one(
        comodel_name='res.opportunity.space', string='Opportunity Space')
    res_character_id = fields.Many2one(
        comodel_name='res.character', string='Character')
    justification_deadline = fields.Date(string='Justification Deadline')
    res_area_type_id = fields.Many2one(
        comodel_name='res.area.type', string='Area type',
        domain="[('area_ids', 'in', res_area_id)]")
    res_team_id = fields.Many2one(
        comodel_name='res.team', string='Team')
    res_target_id = fields.Many2one(
        comodel_name='res.target', string='Target')
    nonoperative = fields.Boolean(
        string='Non Operative', related='res_area_id.nonoperative', store=True)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    nonoperative = fields.Boolean(
        string='Non Operative', related='account_id.nonoperative', store=True)
