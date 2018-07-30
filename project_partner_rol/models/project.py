# Copyright 2018 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
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

    project_location_id = fields.Many2one(
        comodel_name='res.partner', string='Location')
    participant_ids = fields.One2many(
        comodel_name='project.participant',
        inverse_name='project_id', string='Participants')
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
            project.task_date_start = min(
                tasks.filtered(lambda t: t.project_id.id == project.id and
                               t.date_start).mapped('date_start'))
            project.task_date_end = max(
                tasks.filtered(lambda t: t.project_id.id == project.id and
                               t.date_end).mapped('date_end'))
            project.task_date_margin = relativedelta2months(
                relativedelta.relativedelta(
                    str2datetime(project.task_date_end),
                    str2datetime(project.task_date_start)))


class ProjectParticipant(models.Model):
    _name = 'project.participant'
    _description = 'Project participants'
    _rec_name = 'partner_id'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project', required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Participant', required=True)
    rol_id = fields.Many2one(
        comodel_name='project.participant.rol', string='Role')
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
        for participant in self.filtered('planned_hours_percentage'):
            participant.project_planned_hours = (
                participant.project_id.planned_hours *
                (participant.planned_hours_percentage / 100.0))

    @api.multi
    @api.depends('project_id', 'project_id.task_planned_hours',
                 'planned_hours_percentage')
    def _compute_task_planned_hours(self):
        for participant in self.filtered('planned_hours_percentage'):
            participant.task_planned_hours = (
                participant.project_id.task_planned_hours *
                (participant.planned_hours_percentage / 100.0))

    @api.multi
    @api.depends('project_planned_hours', 'project_id',
                 'project_id.planned_date_margin')
    def _compute_monthly_planned_hours(self):
        for participant in self:
            participant.monthly_planned_hours = (
                participant.project_planned_hours /
                participant.project_id.planned_date_margin
                if participant.project_id.planned_date_margin else 0.0)

    @api.multi
    @api.depends('task_planned_hours', 'project_id',
                 'project_id.task_date_margin')
    def _compute_monthly_task_planned_hours(self):
        for participant in self:
            participant.monthly_task_planned_hours = (
                participant.task_planned_hours /
                participant.project_id.task_date_margin
                if participant.project_id.task_date_margin else 0.0)


class ProjectParticipantRol(models.Model):
    _name = 'project.participant.rol'
    _description = 'Roles of project participants'

    name = fields.Char(string='Description', required=True)
