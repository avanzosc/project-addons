# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    verification_criteria_ids = fields.One2many(
        string="Verification criteria",
        comodel_name="project.task.verification.criteria",
        inverse_name="task_id",
        copy=False,
    )
    sheet_number_id = fields.Many2one(
        string="Sheet Number", comodel_name="ir.attachment"
    )
