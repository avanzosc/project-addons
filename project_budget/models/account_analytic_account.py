# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    crossovered_last_budget_line = fields.One2many(
        comodel_name='crossovered.budget.lines',
        inverse_name='analytic_account_id', string='Last budget lines',
        domain=[('show_line', '=', True)])
