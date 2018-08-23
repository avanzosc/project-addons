# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp

from dateutil import relativedelta

str2datetime = fields.Datetime.from_string


def relativedelta2months(delta):
    if not delta:
        return 0.0
    months = delta.months or 0.0
    months += (delta.years or 0.0) * 12
    months += (delta.days or 0.0) / 30
    return months


class ProjectProject(models.Model):
    _inherit = 'project.project'

    member_ids = fields.One2many(
        comodel_name='project.member', inverse_name='project_id',
        string='Members')
    planned_hours = fields.Float(
        string='Initially Planned Hours',
        help='Estimated time to do the task, usually set by the project '
             'manager.')
    task_planned_hours = fields.Float(
        string='Initially Planned Hours',
        help='Estimated time to do the task, usually set by the project '
             'manager when the task is in draft state.',
        compute='_compute_task_planned_hours')
    planned_date_start = fields.Datetime()
    planned_date_end = fields.Datetime()
    planned_date_margin = fields.Float(compute='_compute_planned_dates')
    task_date_start = fields.Datetime(compute='_compute_task_dates')
    task_date_end = fields.Datetime(compute='_compute_task_dates')
    task_date_margin = fields.Float(compute='_compute_task_dates')

    @api.multi
    def _compute_task_planned_hours(self):
        tasks = self.env['project.task'].search([
            ('project_id', 'in', self.ids)])
        for project in self:
            project.task_planned_hours = sum(
                tasks.filtered(lambda t: t.project_id.id == project.id).mapped(
                    'planned_hours'))

    @api.multi
    @api.depends('planned_date_start', 'planned_date_end')
    def _compute_planned_dates(self):
        for project in self.filtered(
                lambda p: p.planned_date_start and p.planned_date_end):
            project.planned_date_margin = relativedelta2months(
                relativedelta.relativedelta(
                    str2datetime(project.planned_date_end),
                    str2datetime(project.planned_date_start)))

    @api.multi
    def _compute_task_dates(self):
        tasks = self.env['project.task'].search([
            ('project_id', 'in', self.ids)])
        for project in self.filtered('task_ids'):
            project_tasks = tasks.filtered(
                lambda t: t.project_id.id == project.id)
            start_dates = (
                project_tasks.filtered('date_start').mapped('date_start'))
            if start_dates:
                project.task_date_start = min(start_dates)
            end_dates = (
                project_tasks.filtered('date_end').mapped('date_end'))
            if end_dates:
                project.task_date_end = max(end_dates)
            project.task_date_margin = relativedelta2months(
                relativedelta.relativedelta(
                    str2datetime(project.task_date_end),
                    str2datetime(project.task_date_start)))


class ProjectMember(models.Model):
    _name = 'project.member'
    _description = 'Project Member'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project', required=True)
    user_id = fields.Many2one(
        comodel_name='res.users', string='Member', required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner',
        related='user_id.partner_id', readonly=True)
    planned_hours_percentage = fields.Float(
        string='Percentage (%)', digits=dp.get_precision('Discount'))
    project_planned_hours = fields.Float(
        string='Initially Planned Hours',
        compute='_compute_project_planned_hours')
    task_planned_hours = fields.Float(
        string='Initially Planned Hours',
        compute='_compute_task_planned_hours')
    monthly_planned_hours = fields.Float(
        string='Monthly Hours',
        compute='_compute_monthly_planned_hours')
    monthly_task_planned_hours = fields.Float(
        string='Monthly Hours',
        compute='_compute_monthly_task_planned_hours')

    @api.multi
    @api.constrains('planned_hours_percentage')
    def _check_percent(self):
        for record in self:
            if (record.planned_hours_percentage < 0.0 or
                    record.planned_hours_percentage > 100.0):
                raise ValidationError(
                    _('Percentages must be between 0 and 100.'))

    @api.multi
    @api.depends('project_id', 'project_id.planned_hours',
                 'planned_hours_percentage')
    def _compute_project_planned_hours(self):
        for record in self.filtered('planned_hours_percentage'):
            record.project_planned_hours = (
                record.project_id.planned_hours *
                (record.planned_hours_percentage / 100.0))

    @api.multi
    @api.depends('project_id', 'project_id.task_planned_hours',
                 'planned_hours_percentage')
    def _compute_task_planned_hours(self):
        for record in self.filtered('planned_hours_percentage'):
            record.task_planned_hours = (
                record.project_id.task_planned_hours *
                (record.planned_hours_percentage / 100.0))

    @api.multi
    @api.depends('project_planned_hours', 'project_id',
                 'project_id.planned_date_margin')
    def _compute_monthly_planned_hours(self):
        for record in self:
            record.monthly_planned_hours = (
                record.project_planned_hours /
                record.project_id.planned_date_margin
                if record.project_id.planned_date_margin else 0.0)

    @api.multi
    @api.depends('task_planned_hours', 'project_id',
                 'project_id.task_date_margin')
    def _compute_monthly_task_planned_hours(self):
        for record in self:
            record.monthly_task_planned_hours = (
                record.task_planned_hours /
                record.project_id.task_date_margin
                if record.project_id.task_date_margin else 0.0)
