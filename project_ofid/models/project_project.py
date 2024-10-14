# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    private_project = fields.Boolean(
        string="Is Private Project?",
        related="type_id.private_project",
        store=True,
        copy=False,
    )
