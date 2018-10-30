# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectTaskPlan(models.Model):
    _name = 'project.task.plan'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', required=True)
    project = fields.Char(string='Project')
    phase_id = fields.Many2many(
        string='Phase', comodel_name='project.task.phase')
    date_min = fields.Datetime(string='Minimal Date', compute='_compute_date')
    date_max = fields.Datetime(string='Maximal Date', compute='_compute_date')

    @api.onchange('project_id')
    def onchange_project_id(self):
        self.project = self.project_id.name

    @api.depends('project_id', 'phase_id')
    def _compute_dates(self):
        for phase_table in self.filtered('project_id'):
            project_tasks = self.env['project.task'].search([
                ('project_id', '=', phase_table.project_id.id)])
            start_dates = (
                project_tasks.filtered('date_start').mapped('date_start'))
            if start_dates:
                phase_table.date_min = min(start_dates)
            end_dates = (
                project_tasks.filtered('date_end').mapped('date_end'))
            if end_dates:
                phase_table.date_max = max(end_dates)
