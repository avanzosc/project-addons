# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class WizChangeProjectTaskDate(models.TransientModel):
    _name = 'wiz.change.project.task.date'
    _description = 'Date changing wizard'

    days = fields.Integer(
        string='Days', required=True,
        help='Positive sum days, negative subtraction days')

    @api.multi
    def button_change_project_task_date(self):
        task_obj = self.env['project.task']
        tasks = task_obj.browse(self.env.context.get('active_ids'))
        tasks._change_project_task_date(self.days)
