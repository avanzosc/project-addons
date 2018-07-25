# Copyright 2018 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp


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

    @api.multi
    def _compute_task_planned_hours(self):
        tasks = self.env['project.task'].search([])
        for project in self:
            project.task_planned_hours = sum(
                tasks.filtered(lambda t: t.project_id.id == project.id).mapped(
                    'planned_hours'))


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

    @api.multi
    @api.constrains('planned_hours_percentage')
    def _check_percent(self):
        for record in self:
            if (record.planned_hours_percentage < 0.0 or
                    record.planned_hours_percentage > 100.0):
                raise ValidationError(
                    _('Percentages for must be between 0 and 100.'))

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

class ProjectParticipantRol(models.Model):
    _name = 'project.participant.rol'
    _description = 'Roles of project participants'

    name = fields.Char(string='Description', required=True)
