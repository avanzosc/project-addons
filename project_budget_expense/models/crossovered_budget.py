# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    @api.multi
    def button_distribute_task_costs(self):
        for budget in self.filtered('project_id'):
            budget_lines = budget.crossovered_budget_line.filtered(
                'general_budget_id.expenses')
            budget_lines.distribute_task_cost()
