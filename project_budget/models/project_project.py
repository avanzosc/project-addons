# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
import calendar

to_string = fields.Date.to_string
from_string = fields.Date.from_string


class ProjectProject(models.Model):
    _inherit = 'project.project'

    budget_ids = fields.One2many(
        comodel_name='crossovered.budget', inverse_name='project_id',
        string='Budgets')
    budget_count = fields.Integer(
        string='# Budgets', compute='_compute_budget_count')
    current_budget_id = fields.Many2one(
        string='Current Budget', comodel_name='crossovered.budget',
        compute='_compute_budget_count')
    current_budget_count = fields.Integer(
        string='# Current Budgets', compute='_compute_budget_count')
    has_current_budget = fields.Boolean(
        string='Has Current Budget', compute='_compute_budget_count',
        search='_search_current_budget')

    @api.multi
    def _compute_budget_count(self):
        today = from_string(fields.Date.context_today(self))
        month_start = to_string(today.replace(day=1))
        month_end = \
            to_string(today.replace(
                day=calendar.monthrange(today.year, today.month)[1]))
        for record in self:
            record.budget_count = len(
                record.with_context(active_test=False).budget_ids)
            record.current_budget_id = record.budget_ids.filtered(
                lambda b: b.budget_date >= month_start and
                          b.budget_date <= month_end)[:1]
            record.current_budget_count = len(record.current_budget_id)
            record.has_current_budget = bool(record.current_budget_id)

    @api.multi
    def _search_current_budget(self, operator, value):
        today = from_string(fields.Date.context_today(self))
        month_start = to_string(today.replace(day=1))
        month_end = \
            to_string(today.replace(
                day=calendar.monthrange(today.year, today.month)[1]))
        current_budgets = self.env['crossovered.budget'].search([
            ('project_id', '<>', False),
            ('budget_date', '>=', month_start),
            ('budget_date', '<=', month_end)])
        operator = 'in' if ((operator == '=' and value) or
                            (operator == '!=' and not value)) else 'not in'
        return [('id', operator, current_budgets.mapped('project_id').ids)]

    @api.multi
    def create_initial_project_budget(self, date=False):
        if not date:
            date = fields.Date.context_today(self)
        budget_obj = self.env['crossovered.budget']
        budget_date = from_string(date)
        date_from = to_string(budget_date.replace(month=1, day=1))
        date_to = to_string(budget_date.replace(month=12, day=31))
        for record in self.filtered(lambda l: not any(l.budget_ids.filtered(
                lambda b: b.initial and b.year == budget_date.year))):
            budget = budget_obj.create({
                'name': _(
                    u'Initial {} budget: {}').format(budget_date.year,
                                                     record.name),
                'initial': True,
                'creating_user_id': record.user_id.id,
                'date_from': date_from,
                'date_to': date_to,
                'budget_date': budget_date,
                'project_id': record.id,
            })
            budget.button_compute_lines()

    @api.model
    def create(self, values):
        created = super(ProjectProject, self).create(values)
        created.create_initial_project_budget()
        return created
