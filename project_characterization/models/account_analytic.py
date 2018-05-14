# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    res_area_id = fields.Many2one(
        comodel_name='res.area', string='Area')
    res_space_id = fields.Many2one(
        comodel_name='res.space', string='Space')
    res_character_id = fields.Many2one(
        comodel_name='res.character', string='Character')
    funding_source_id = fields.Many2one(
        comodel_name='funding.source', string='Funding Source')
    department_id = fields.Many2one(
        comodel_name='hr.department', string='Internal Services Department')
    justification_deadline = fields.Date(string='Justification Deadline')
    res_area_type_id = fields.Many2one(
        comodel_name='res.area.type', string='Area type',
        domain="[('area_ids', 'in', res_area_id)]")
    res_team_id = fields.Many2one(
        comodel_name='res.team', string='Team')
    crm_team_id = fields.Many2one(
        comodel_name='crm.team', string='Team (CRM)')
    res_target_id = fields.Many2one(
        comodel_name='res.target', string='Target')
