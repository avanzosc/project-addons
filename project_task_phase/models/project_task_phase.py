# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectTaskPhase(models.Model):
    _inherit = 'project.project'

    phase_table_ids = fields.One2many(
        comodel_name='project.task.plan', inverse_name='project_id')
    date_min = fields.Datetime(string='Minimal date', compute='_compute_dates')
    date_max = fields.Datetime(string='Maximal date', compute='_compute_dates')

    @api.depends('phase_table_ids')
    def _compute_dates(self):
        for project in self.filtered('phase_table_ids'):
            start_dates = (
                project.mapped('phase_table_ids.date_min'))
            if start_dates:
                project.date_min = min(start_dates)
            end_dates = (
                project.mapped('phase_table_ids.date_max'))
            if end_dates:
                project.date_max = max(end_dates)
