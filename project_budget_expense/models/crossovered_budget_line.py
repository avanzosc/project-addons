# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class CrossoveredBudgetLine(models.Model):
    _inherit = "crossovered.budget.lines"

    @api.multi
    def distribute_task_cost(self):
        calendar_model = self.env["project.task.calendar"]
        for line in self.filtered(lambda l: l.general_budget_id.expenses and
                                  l.crossovered_budget_id.project_id):
            project = line.crossovered_budget_id.project_id
            period_lines = calendar_model.search(
                [("project_id", "=", project.id),
                 ("date", ">=", line.date_from),
                 ("date", "<=", line.date_to)])
            line.write({
                'planned_amount': (
                    -1 * sum(period_lines.mapped('planned_cost'))),
            })
