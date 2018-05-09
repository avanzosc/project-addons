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
                line.parent_budget_line_id = line.id
                vals.update({
                    'general_budget_id': income.id,
                })
                line = budget_line_obj.create(vals)
                line.parent_budget_line_id = line.id
                ds = ds + relativedelta(months=1)
            if to_string(final_date) < budget.date_to:
                vals.update({
                    'date_from': to_string(final_date),
                    'date_to': to_string(final_date),
                    'general_budget_id': postcome.id,
                })
                line = budget_line_obj.create(vals)
                line.parent_budget_line_id = line.id
                vals.update({
                    'general_budget_id': income.id,
                })
                line = budget_line_obj.create(vals)
                line.parent_budget_line_id = line.id
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


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"
    _description = "Budget Line"

    @api.multi
    @api.depends('analytic_account_id',
                 'analytic_account_id.crossovered_budget_line')
    def _compute_show_line(self):
        for line in self:
            line.show_line = False
            budget_line = max(
                line.analytic_account_id.mapped('crossovered_budget_line'),
                key=lambda x: x.crossovered_budget_id.id)
            if (budget_line and line.crossovered_budget_id.id ==
                    budget_line.crossovered_budget_id.id):
                line.show_line = True

    parent_budget_line_id = fields.Many2one(
        comodel_name='crossovered.budget.lines', string='Parent budget line',
        copy=True)
    initial_planned_amount = fields.Float(
        'Initial planned amount', digits=0, store=True,
        related='parent_budget_line_id.planned_amount')
    show_line = fields.Boolean(
        string='Show line', compute='_compute_show_line', store=True)
    notes = fields.Text(string='Notes')
    project_id = fields.Many2one(
        comodel_name='project.project', string='Project',
        related='crossovered_budget_id.project_id', store=True)
