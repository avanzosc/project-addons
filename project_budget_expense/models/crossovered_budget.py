# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    @api.multi
    def button_distribute_task_costs(self):
        task_model = self.env['project.task']
        for budget in self.filtered('project_id'):
            tasks = task_model.search([
                ('project_id', '=', budget.project_id.id)])
            project_cost = sum(tasks.mapped('planned_cost'))
            budget_lines = budget.crossovered_budget_line.filtered(
                'general_budget_id.expenses')
            if budget_lines:
                budget_lines.write({
                    'planned_amount': (
                        project_cost / len(budget_lines)),
                })
