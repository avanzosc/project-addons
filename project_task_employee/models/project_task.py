# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    employee_id = fields.Many2one(
        string="Employee", comodel_name="hr.employee", copy=False)

    @api.onchange("employee_id")
    def _onchange_employee_id(self):
        if self.employee_id and self.employee_id.user_id:
            self.user_id = self.employee_id.user_id.id
