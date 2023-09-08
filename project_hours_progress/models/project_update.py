# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProjectUpdate(models.Model):
    _inherit = "project.update"

    milestones_progress = fields.Float(
        string="Milestones Progress", copy=False)

    def default_get(self, fields):
        result = super().default_get(fields)
        if result.get("project_id"):
            project = self.env["project.project"].browse(
                result["project_id"])
            if "progress" in fields:
                result["progress"] = project.tasks_progress
            if "milestones_progress" in fields:
                result["milestones_progress"] = project.milestones_progress
        return result
