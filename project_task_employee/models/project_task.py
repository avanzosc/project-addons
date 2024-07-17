from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    responsible_id = fields.Many2one("hr.employee", string="Responsible")
