# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, exceptions, fields, models
from dateutil.relativedelta import relativedelta

to_string = fields.Date.to_string
from_string = fields.Date.from_string


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project',
        states={'done': [('readonly', True)]})
    initial = fields.Boolean(
        string='Initial', copy=False, states={'done': [('readonly', True)]})
    active = fields.Boolean(string='Active', default=True)
    year = fields.Integer(string='Year', compute='_compute_year', store=True)
    budget_date = fields.Date(
        string='Budget Date', default=lambda s: fields.Date.context_today(s))

    @api.depends('date_from')
    def _compute_year(self):
        for record in self:
            record.year = from_string(record.date_from).year

    @api.multi
    def action_create_period(self):
        budget_line_obj = self.env['crossovered.budget.lines']
        postcome = self.env.ref('project_budget.budget_post_postcome')
        income = self.env.ref('project_budget.budget_post_income')
        for budget in self.filtered(lambda b: b.project_id and not
                                    b.crossovered_budget_line and
                                    b.state == 'draft'):
            vals = {
                'analytic_account_id':
                budget.project_id.analytic_account_id.id,
                'crossovered_budget_id': budget.id,
                'planned_amount': 0.0,
            }
            ds = from_string(budget.date_from)
            final_date = ds.replace(day=30, month=12)
            while to_string(ds) < budget.date_to:
                de = ds + relativedelta(months=1, days=-1)
                if to_string(de) > budget.date_to:
                    de = from_string(budget.date_to)
                vals.update({
                    'date_from': to_string(ds),
                    'date_to': to_string(de),
                    'general_budget_id': postcome.id,
                })
                line = budget_line_obj.create(vals)
                line.initial_budget_line_id = line.id
                vals.update({
                    'general_budget_id': income.id,
                })
                line = budget_line_obj.create(vals)
                line.initial_budget_line_id = line.id
                ds = ds + relativedelta(months=1)
            if to_string(final_date) < budget.date_to:
                vals.update({
                    'date_from': to_string(final_date),
                    'date_to': to_string(final_date),
                    'general_budget_id': postcome.id,
                })
                line = budget_line_obj.create(vals)
                line.initial_budget_line_id = line.id
                vals.update({
                    'general_budget_id': income.id,
                })
                line = budget_line_obj.create(vals)
                line.initial_budget_line_id = line.id
        return True

    @api.multi
    @api.constrains('project_id', 'initial', 'date_from')
    def _check_initial_by_project(self):
        for record in self.filtered('project_id'):
            if len(self.search([('project_id', '=', record.project_id.id),
                                ('initial', '=', True),
                                ('year', '=', record.year)])) > 1:
                raise exceptions.ValidationError(
                    _("There can only be one initial budget per project and "
                      "year."))

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        new = super(CrossoveredBudget, self).copy(default=default)
        self.filtered(lambda b: not b.initial).write({
            'active': False,
        })
        return new

    @api.multi
    def open_pivot_view(self):
        self.ensure_one()
        action = self.env.ref(
            'account_budget.act_crossovered_budget_lines_view')
        action_dict = action.read()[0]
        action_dict.update({
            'view_mode': 'pivot',
            'view_id': False,
            'views': [],
            'domain': [('crossovered_budget_id', '=', self.id)],
        })
        return action_dict


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    initial_budget_line_id = fields.Many2one(
        comodel_name='crossovered.budget.lines', string='Initial Budget Line',
        copy=True)
    initial_planned_amount = fields.Float(
        string='Initial Planned Amount', digits=0, store=True,
        related='initial_budget_line_id.planned_amount')
    notes = fields.Text(string='Notes')
    project_id = fields.Many2one(
        comodel_name='project.project', string='Project',
        related='crossovered_budget_id.project_id', store=True)
    sum_amount = fields.Float(
        string='Amount Sum', compute='_compute_sum_amount')
    budget_active = fields.Boolean(
        string='Budget Active',
        related='crossovered_budget_id.active', store=True)
    budget_date = fields.Date(
        string='Budget Date',
        related='crossovered_budget_id.budget_date', store=True)

    @api.depends('planned_amount', 'practical_amount')
    def _compute_sum_amount(self):
        for record in self:
            record.sum_amount = (
                record.planned_amount + record.practical_amount)
