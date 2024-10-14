# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    private_project = fields.Boolean(
        string="Is Private Project?",
        related="project_id.private_project",
        store=True,
        copy=False,
    )
