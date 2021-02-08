# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from dateutil.relativedelta import relativedelta
from datetime import timedelta
from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)
str2date = fields.Date.from_string

try:
    from odoo.addons.queue_job.job import job
except ImportError:
    _logger.debug('Can not `import queue_job`.')
    import functools

    def empty_decorator_factory(*argv, **kwargs):
        return functools.partial
    job = empty_decorator_factory


class ProjectTask(models.Model):
    _inherit = 'project.task'

    employee_cost = fields.Float(string='Employee Cost', copy=False)
    planned_cost = fields.Float(
        string='Estimated Cost', compute='_compute_planned_cost', store=True)
    effective_cost = fields.Float(
        string='Real Cost', compute='_compute_effective_cost', store=True)
    planned_monthly_hours = fields.Float(
        string='Planned Monthly Hours',
        compute='_compute_planned_monthly_hours', store=True)
    calendar_ids = fields.One2many(
        comodel_name='project.task.calendar', inverse_name='task_id')

    @api.onchange('user_id')
    def _onchange_user(self):
        res = super(ProjectTask, self)._onchange_user()
        self.button_update_employee_cost()
        return res

    @api.depends('user_id', 'employee_cost', 'planned_hours')
    def _compute_planned_cost(self):
        for task in self.filtered('user_id'):
            task.planned_cost = task.planned_hours * task.employee_cost

    @api.depends('user_id', 'timesheet_ids', 'timesheet_ids.amount')
    def _compute_effective_cost(self):
        for task in self.filtered('user_id'):
            task.effective_cost = abs(sum(task.mapped('timesheet_ids.amount')))

    @api.depends('date_start', 'date_end', 'planned_hours')
    def _compute_planned_monthly_hours(self):
        for task in self.filtered(lambda t: t.date_start and t.date_end):
            datedelta = relativedelta(
                str2date(task.date_end), str2date(task.date_start))
            months = (datedelta.years * 12) + datedelta.months
            if months and datedelta.days >= 15:
                months += 1
            task.planned_monthly_hours = round(
                task.planned_hours / (months or 1.0), 2)

    @api.multi
    def button_update_employee_cost(self):
        employee_model = self.env['hr.employee']
        for task in self.filtered('user_id'):
            employee = employee_model.search(
                [('user_id', '=', task.user_id.id)], limit=1)
            task.employee_cost = employee.timesheet_cost

    @api.multi
    def button_recompute_costs(self):
        fields_list = ['effective_cost']
        for field in fields_list:
            self.env.add_todo(self._fields[field], self)
        self.recompute()

    @job()
    def button_create_calendar(self):
        for task in self.filtered(lambda t: t.date_start and t.date_end):
            task.calendar_ids.unlink()
            date_start = str2date(task.date_start)
            date_end = str2date(task.date_end)
            date_list = [date_start + timedelta(days=d)
                         for d in range((date_end - date_start).days + 1)]
            task.write({
                "calendar_ids": [(0, 0, {
                    "date": x,
                    "task_id": task.id}) for x in date_list],
            })
            timesheets = task.timesheet_ids.filtered(
                lambda s: s.date < task.date_start or s.date > task.date_end)
            timesheets.create_calendar()

    @api.multi
    def _cleanup_calendar(self):
        logger.info('Cleanup Task Calendar.')
        date_tasks = self.search([
            ('date_start', '!=', False),
            ('date_end', '!=', False),
            ('timesheet_ids', '!=', False),
            ('calendar_ids', '!=', False)
        ])
        calendars = calendar_obj = self.env["project.task.calendar"]
        for task in date_tasks:
            calendars |= calendar_obj.search([
                ("task_id", "=", task.id),
                '|', ("date", "<", task.date_start),
                ("date", ">", task.date_end),
                ("date", "not in", task.mapped("timesheet_ids.date")),
            ])
        calendars.unlink()
        logger.info('Task Calendar cleanup finished.')

    @api.model
    def create(self, vals):
        task = super(ProjectTask, self).create(vals)
        if 'date_start' in vals and 'date_end' in vals:
            task.with_delay().button_create_calendar()
        return task

    @api.multi
    def write(self, vals):
        result = super(ProjectTask, self).write(vals)
        if 'date_start' in vals or 'date_end' in vals:
            self.with_delay().button_create_calendar()
        return result
