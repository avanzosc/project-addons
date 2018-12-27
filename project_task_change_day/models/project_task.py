# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

str2datetime = fields.Datetime.from_string


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def _change_project_task_date(self, new_days):
        for task in self:
            new_start_date = (str2datetime(task.date_start) +
                              relativedelta(days=new_days))
            new_end_date = (str2datetime(task.date_end) +
                            relativedelta(days=new_days))
            vals = {'date_start': new_start_date,
                    'date_end': new_end_date}
            task.write(vals)
