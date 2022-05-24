# Copyright 2019 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models

str2date = fields.Date.from_string


class ProjectTaskCalendar(models.Model):
    _name = 'project.task.calendar'
    _description = 'Task Calendar'
    _order = 'task_id, date'

    @api.model
    def _get_selection_dayofweek(self):
        return self.env['resource.calendar.attendance'].fields_get(
            allfields=['dayofweek'])['dayofweek']['selection']

    task_id = fields.Many2one(
        comodel_name='project.task', string='Task', required=True,
        ondelete='cascade')
    project_id = fields.Many2one(
        comodel_name='project.project', string='Project',
        related='task_id.project_id', store=True)
    project_code = fields.Char(
        string='Reference', related='task_id.project_id.code', store=True)
    project_parent_id = fields.Many2one(
        comodel_name='res.partner', string='Customer',
        related='task_id.project_id.partner_id', store=True)
    project_phase_id = fields.Many2one(
        comodel_name='project.phase', string='Project Phase',
        related='task_id.project_id.phase_id', store=True)
    date = fields.Date(string='Date', required=True)
    dayofweek = fields.Selection(
        selection='_get_selection_dayofweek', string='Day of Week', index=True,
        compute='_compute_dayofweek', store=True)
    user_leave = fields.Boolean(
        string='Holidays', compute='_compute_user_leave', store=True)
    user_id = fields.Many2one(
        comodel_name='res.users', string='Assigned to',
        related='task_id.user_id', store=True)
    planned_hours = fields.Float(
        string='Planned Hours', compute='_compute_planned_cost', store=True)
    effective_hours = fields.Float(
        string='Hours Spent', compute='_compute_effective_cost', store=True)
    employee_cost = fields.Float(
        string='Employee Cost', related='task_id.employee_cost', store=True)
    planned_cost = fields.Float(
        string='Planned Cost', compute='_compute_planned_cost', store=True)
    effective_cost = fields.Float(
        string='Effective Cost', compute='_compute_effective_cost', store=True)
    workhours = fields.Float(
        string='Workhours', compute='_compute_workhours', store=True)

    @api.depends('date')
    def _compute_dayofweek(self):
        for line in self.filtered('date'):
            line.dayofweek = str(str2date(line.date).weekday())

    @api.depends('date', 'user_id')
    def _compute_user_leave(self):
        resource_model = self.env['resource.resource']
        leave_model = self.env['resource.calendar.leaves']
        for line in self:
            user = line.task_id.user_id
            resources = resource_model.search([('user_id', '=', user.id)])
            leaves = leave_model.search([
                '|', ('resource_id', 'in', resources.ids),
                ('resource_id', '=', False),
                ('date_from', '<=', line.date), ('date_to', '>=', line.date)])
            line.user_leave = leaves

    @api.depends('user_id', 'dayofweek', 'user_leave')
    def _compute_workhours(self):
        employee_model = self.env['hr.employee']
        for line in self.filtered(lambda l: not l.user_leave):
            employee = employee_model.search(
                [('user_id', '=', line.task_id.user_id.id)], limit=1)
            attendances = employee.mapped(
                'resource_calendar_id.attendance_ids').filtered(
                lambda a: a.dayofweek == line.dayofweek)
            line.workhours = sum([(a.hour_to - a.hour_from)
                                  for a in attendances])

    @api.depends('user_leave', 'task_id', 'task_id.planned_hours',
                 'task_id.calendar_ids', 'employee_cost')
    def _compute_planned_cost(self):
        employee_model = self.env['hr.employee']
        for line in self.filtered(lambda l: not l.user_leave):
            user = line.task_id.user_id
            employee = employee_model.search(
                [('user_id', '=', user.id)], limit=1)
            weekdays = employee.resource_calendar_id.mapped(
                'attendance_ids.dayofweek')
            if (line.dayofweek in weekdays and
                    (line.task_id.date_start and
                     line.date >= line.task_id.date_start.date()) and
                    (line.task_id.date_end and
                     line.date <= line.task_id.date_end.date())):
                line_count = len(line.task_id.calendar_ids.filtered(
                    lambda l: l.dayofweek in weekdays and not l.user_leave and
                    l.date >= l.task_id.date_start.date() and
                    l.date <= l.task_id.date_end.date()))
                line.planned_hours = (line.task_id.planned_hours /
                                      (line_count or 1))
                line.planned_cost = line.planned_hours * line.employee_cost

    @api.depends('task_id', 'task_id.timesheet_ids',
                 'task_id.timesheet_ids.unit_amount',
                 'task_id.timesheet_ids.amount')
    def _compute_effective_cost(self):
        for line in self:
            timesheets = line.task_id.timesheet_ids.filtered(
                lambda t: t.date == line.date)
            line.effective_hours = sum(timesheets.mapped('unit_amount'))
            line.effective_cost = abs(sum(timesheets.mapped('amount')))
