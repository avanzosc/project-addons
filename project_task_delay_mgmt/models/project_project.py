# Copyright 2022 Patxi Lersundi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    date_limit = fields.Date(
        string='Date limit', compute='_compute_date_limit',
        copy=False,
        store=True,
        readonly=True
        )
    global_delay = fields.Integer(
        string='Tasks global delay (days)', compute='_compute_global_delay',
        copy=False,
        store=True,
        readonly=True
        )

    @api.depends("task_ids", "task_ids.date_deadline")
    def _compute_date_limit(self):
        for project in self:
            for task in project.task_ids.filtered(lambda t: t.date_deadline):
                if not project.date_limit or (
                                task.date_deadline > project.date_limit):
                    project.date_limit = task.date_deadline

    @api.depends("task_ids", "task_ids.task_delay")
    def _compute_global_delay(self):
        for project in self:
            project.global_delay = sum(project.task_ids.mapped('task_delay'))
