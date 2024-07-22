# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProjectTaskVerificationCriteria(models.Model):
    _name = "project.task.verification.criteria"
    _description = "Project task verification criteria"

    task_id = fields.Many2one(
        string="Task",
        comodel_name="project.task",
        required=True,
        copy=False,
    )
    dimensions = fields.Text(string="Dimensions", copy=False)
    nominal_value = fields.Float(string="Nominal value", copy=False)
    real_value = fields.Float(string="Real value", copy=False)
    initial_measurement = fields.Float(string="Initial measurement", copy=False)
    average_measurement = fields.Float(string="Average measurement", copy=False)
    final_measurement = fields.Float(string="Final measurement", copy=False)
    date_hour = fields.Datetime(string="Date and hour", copy=False)
    responsible_inspection_id = fields.Many2one(
        string="Responsible inspection",
        comodel_name="hr.employee",
        copy=False,
    )
