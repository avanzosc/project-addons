# Copyright 2022 Patxi Lersundi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from datetime import timedelta


class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_delay = fields.Integer(
        string='Task delay (days)', compute='_compute_task_delay',
        copy=False,
        store=True,
        )

    @api.depends("date_deadline", "date_end")
    def _compute_task_delay(self):
        for task in self:
            if task.date_end and task.date_deadline:
                task.task_delay = (
                    task.date_end.date()-task.date_deadline)/timedelta(days=1)
