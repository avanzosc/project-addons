# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectTaskPhaseTable(models.Model):
    _name = 'project.task.phase.table'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', required=True)
    project = fields.Char(string='Project')
    phase = fields.Many2many(
        string='Phase', comodel_name='project.task.milestone.phase')
    date_start = fields.Char(string='Start Date')
    date_end = fields.Date(string='End Date')
    date_min = fields.Date(string='Minimal Date')
    date_max = fields.Date(string='Maximal Date')

    @api.onchange('project_id')
    def onchange_project_id(self):
        self.project = self.project_id.name

    @api.multi
    def _mindate(self):
        for date in self.date_start:
            self.date_min = min(date)

    @api.multi
    def _maxdate(self):
        for date in self.date_end:
            self.date_max = min(date)
