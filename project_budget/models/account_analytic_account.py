# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _domain_budget_line(self):
        if not self:
            return []
        all_lines = self.env['crossovered.budget.lines'].search(
            [('analytic_account_id', '=', self.id)])
        last_budget = all_lines.mapped('crossovered_budget_id')[-1:]
        domain = (
            [('crossovered_budget_id', '=', last_budget.id)] if last_budget
            else [])
        return domain

    crossovered_budget_line = fields.One2many(
        domain=lambda self: self._domain_budget_line())
