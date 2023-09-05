# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    timesheet_encode_uom_id = fields.Many2one(
        comodel_name="uom.uom", related="company_id.timesheet_encode_uom_id"
    )
    total_timesheet_time = fields.Integer(
        compute="_compute_total_timesheet_time",
        help="Total number of time (in the proper UoM) recorded in the project, rounded"
        " to the unit.",
    )
    timesheet_report_ids = fields.One2many(
        comodel_name="project.task.timesheet.report",
        inverse_name="task_id",
    )

    @api.depends("timesheet_ids")
    def _compute_total_timesheet_time(self):
        for task in self:
            total_time = 0.0
            for timesheet in task.timesheet_ids:
                # Timesheets may be stored in a different unit of measure, so first
                # we convert all of them to the reference unit
                total_time += (
                    timesheet.unit_amount * timesheet.product_uom_id.factor_inv
                )
            # Now convert to the proper unit of measure set in the settings
            total_time *= task.timesheet_encode_uom_id.factor
            task.total_timesheet_time = int(round(total_time))
