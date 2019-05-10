# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

str2date = fields.Date.from_string


class ProjectBudgetSearch(models.TransientModel):
    _name = 'project.budget.search'
    _description = 'Wizard to Search Project by Budget Dates'

    min_date = fields.Date(
        string='Min. Date', required=True,
        default=lambda self: fields.Date.context_today(self))
    max_date = fields.Date(string='Max. Date')
    initial_budget = fields.Boolean(
        string='Initial Budget',
        help='Checking this will search only those with initial budgets')

    @api.multi
    def search_project_budget(self, operator='in'):
        budget_obj = self.env['crossovered.budget']
        projects = self.env['project.project']
        action = self.env.ref('project.open_view_project_all')
        action_dict = action.read()[0] if action else {}
        for record in self:
            min_date = str2date(record.min_date)
            max_date = str2date(record.max_date or record.min_date)
            budget_domain = [
                ('project_id', '<>', False),
                ('budget_date', '>=', min_date),
                ('budget_date', '<=', max_date),
            ]
            if record.initial_budget:
                budget_domain = expression.AND([
                    [('initial', '=', True)],
                    budget_domain])
            budgets = budget_obj.search(budget_domain)
            projects |= budgets.mapped('project_id')
        domain = expression.AND([
            [('id', operator, projects.ids)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain})
        return action_dict

    def search_project_not_in_budget(self):
        return self.search_project_budget(operator='not in')
