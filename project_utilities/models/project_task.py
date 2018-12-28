# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

str2datetime = fields.Datetime.from_string


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def _change_project_task_date(self, new_days):
        for task in self:
            vals = {}
            if task.date_start:
                vals['date_start'] = (str2datetime(task.date_start) +
                                      relativedelta(days=new_days))
            if task.date_end:
                vals['date_end'] = (str2datetime(task.date_end) +
                                    relativedelta(days=new_days))
            if vals:
                task.write(vals)
