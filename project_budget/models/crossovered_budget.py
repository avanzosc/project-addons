# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, exceptions, fields, models

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
        super(CrossoveredBudget, self).action_create_period()
        budget_line_obj = self.env['crossovered.budget.lines']
        for budget in self.filtered(lambda b: b.project_id and
                                    b.state == 'draft'):
            budget.crossovered_budget_line.write({
                'analytic_account_id':
                budget.project_id.analytic_account_id.id,
            })
            get_param = self.env['ir.config_parameter'].sudo().get_param
            if get_param('project_budget.summary_line',
                         'False').lower() == 'true':
                budget_posts = budget.budget_tmpl_id.budget_post_ids
                vals = {
                    'analytic_account_id':
                    budget.project_id.analytic_account_id.id,
                    'crossovered_budget_id': budget.id,
                    'planned_amount': 0.0,
                }
                ds = from_string(budget.date_from)
                final_date = ds.replace(day=30, month=12)
                if to_string(final_date) < budget.date_to:
                    for budget_post in budget_posts:
                        vals.update({
                            'date_from': to_string(final_date),
                            'date_to': to_string(final_date),
                            'general_budget_id': budget_post.id,
                        })
                        budget_line_obj.create(vals)
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
    def button_recompute_line_amount(self):
        self.mapped('crossovered_budget_line').button_recompute_amount()

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
        comodel_name='crossovered.budget.lines', string='Initial Budget Line')
    initial_planned_amount = fields.Float(
        string='Initial Planned Amount', digits=0, store=True,
        compute='_compute_initial_planned_amount')
    notes = fields.Text(string='Notes')
    project_id = fields.Many2one(
        comodel_name='project.project', string='Project',
        related='crossovered_budget_id.project_id', store=True)
    sum_amount = fields.Float(
        string='Amount Sum', compute='_compute_sum_amount', store=True)
    budget_active = fields.Boolean(
        string='Budget Active',
        related='crossovered_budget_id.active', store=True)
    budget_date = fields.Date(
        string='Budget Date',
        related='crossovered_budget_id.budget_date', store=True)
    practical_amount = fields.Float(store=True)

    @api.multi
    def button_recompute_amount(self):
        fields_list = ['practical_amount', 'sum_amount']
        for field in fields_list:
            self.env.add_todo(self._fields[field], self)
        self.recompute()

    @api.depends('initial_budget_line_id', 'planned_amount',
                 'initial_budget_line_id.planned_amount')
    def _compute_initial_planned_amount(self):
        for line in self:
            line.initial_planned_amount = (
                line.initial_budget_line_id.planned_amount
                if line.initial_budget_line_id else line.planned_amount)

    @api.multi
    @api.returns(None, lambda value: value[0])
    def copy_data(self, default=None):
        self.ensure_one()
        default = default or {}
        default.update({
            'initial_budget_line_id':
                self.initial_budget_line_id.id or self.id,
        })
        return super(CrossoveredBudgetLines, self).copy_data(default=default)

    @api.depends('planned_amount', 'practical_amount')
    def _compute_sum_amount(self):
        for record in self:
            record.sum_amount = (
                record.planned_amount + record.practical_amount)
