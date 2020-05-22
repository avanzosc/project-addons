# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    resume_ids = fields.One2many(
        string='Resume', comodel_name='project.task.resume',
        inverse_name='project_id', readonly=True)
    code = fields.Char(
        string='Reference', track_visibility='onchange', index=True)

    @api.multi
    def button_create_task_calendar(self):
        self.mapped('task_ids').button_create_calendar()

    @api.multi
    def button_recompute_costs(self):
        self.mapped('task_ids').button_recompute_costs()
