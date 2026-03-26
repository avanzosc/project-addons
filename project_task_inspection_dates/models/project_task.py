from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    inspection_date = fields.Date()
    next_inspection_date = fields.Date()
    correction_date = fields.Date()
