# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class CrossoveredBudgetLines(models.Model):
    _inherit = 'crossovered.budget.lines'

    res_area_id = fields.Many2one(
        comodel_name='res.area', string='Area',
        related='analytic_account_id.res_area_id', store=True)
    res_area_type_id = fields.Many2one(
        comodel_name='res.area.type', string='Area Type',
        related='analytic_account_id.res_area_type_id', store=True)
    res_team_id = fields.Many2one(
        comodel_name='res.team', string='Team',
        related='analytic_account_id.res_team_id', store=True)
