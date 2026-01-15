from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    building_id = fields.Many2one(
        "res.partner",
        string="Building",
        help="Select the building related to this task.",
    )
