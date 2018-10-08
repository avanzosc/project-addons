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
        string='Budgets', compute='_compute_budget_count')
    current_budget_id = fields.Many2one(
        comodel_name='crossovered.budget', compute='_compute_budget_count')
    current_budget_count = fields.Integer(
        string='Budgets', compute='_compute_budget_count')

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
                          b.budget_date <= month_end)
            record.current_budget_count = len(record.current_budget_id)

    @api.multi
    def create_initial_project_budget(self):
        budget_obj = self.env['crossovered.budget']
        today = from_string(fields.Date.context_today(self))
        date_from = to_string(today.replace(month=1, day=1))
        date_to = to_string(today.replace(month=12, day=31))
        for record in self.filtered(lambda l: not any(l.budget_ids.filtered(
                lambda b: b.initial and b.year == today.year))):
            budget = budget_obj.create({
                'name': _(
                    u'Initial {} budget: {}').format(today.year, record.name),
                'initial': True,
                'creating_user_id': record.user_id.id,
                'date_from': date_from,
                'date_to': date_to,
                'project_id': record.id,
            })
            budget.action_create_period()

    @api.model
    def create(self, values):
        created = super(ProjectProject, self).create(values)
        created.create_initial_project_budget()
        return created
