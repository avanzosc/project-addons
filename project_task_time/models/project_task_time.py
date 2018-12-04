# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

str2date = fields.Datetime.from_string


class ProjectTask(models.Model):
    _inherit = 'project.task'

    employee_cost = fields.Float(string='Employee Cost', readonly=True)
    planned_cost = fields.Float(
        string='Estimated cost', compute='_compute_planned_cost')
    effective_cost = fields.Float(
        string='Real hour cost', compute='_compute_effective_cost')
    planned_monthly_hours = fields.Float(
        string='Estimated Hours', compute='_compute_planned_monthly_hours')

    @api.onchange('user_id')
    def _onchange_user(self):
        res = super(ProjectTask, self)._onchange_user()
        employee_model = self.env['hr.employee']
        for task in self:
            employee = employee_model.search(
                [('user_id', '=', task.user_id.id)], limit=1)
            task.employee_cost = employee.timesheet_cost
        return res

    @api.depends('employee_cost', 'planned_hours')
    def _compute_planned_cost(self):
        for task in self.filtered('user_id'):
            task.planned_cost = task.planned_hours * task.employee_cost

    @api.depends('employee_cost', 'effective_hours')
    def _compute_effective_cost(self):
        for task in self.filtered('user_id'):
            task.effective_cost = task.effective_hours * task.employee_cost

    @api.depends('date_start', 'date_end', 'planned_hours')
    def _compute_planned_monthly_hours(self):
        for task in self.filtered(lambda t: t.date_start and t.date_end):
            months = (
                relativedelta(str2date(task.date_end),
                              str2date(task.date_start)).months + 1)
            task.planned_monthly_hours = task.planned_hours / months
