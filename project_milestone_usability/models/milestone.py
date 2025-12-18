# Copyright 2025 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    tasks_missing = fields.Integer(
        string="Missing Tasks",
        compute="_compute_tasks_missing",
        store=True,
        help="Difference between total tasks and completed tasks.",
    )

    @api.depends("task_count", "done_task_count")
    def _compute_tasks_missing(self):
        for milestone in self:
            milestone.tasks_missing = (milestone.task_count or 0) - (
                milestone.done_task_count or 0
            )
