# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    @api.multi
    def button_distribute_task_costs(self):
        calendar_model = self.env['project.task.calendar']
        for budget in self.filtered('project_id'):
            budget.project_id.sudo().button_create_task_calendar()
            calendar_lines = calendar_model.search([
                ('project_id', '=', budget.project_id.id)])
            budget_lines = budget.crossovered_budget_line.filtered(
                'general_budget_id.expenses')
            for budget_line in budget_lines:
                period_lines = calendar_lines.filtered(
                    lambda l:
                    budget_line.date_from <= l.date <= budget_line.date_to)
                budget_line.write({
                    'planned_amount': (
                        -1 * sum(period_lines.mapped('planned_cost'))),
                })
