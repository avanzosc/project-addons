# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class WizChangeProjectTaskDate(models.TransientModel):
    _name = 'wiz.change.project.task.date'
    _description = 'Date changing wizard'

    days = fields.Integer(
        string='Days',
        help='Positive sum days, negative subtraction days')
    start_days = fields.Integer()
    end_days = fields.Integer()
    start_date = fields.Datetime()
    end_date = fields.Datetime()

    @api.multi
    def button_change_project_task_date(self):
        task_obj = self.env['project.task']
        tasks = task_obj.browse(self.env.context.get('active_ids'))
        if self.days:
            tasks._change_project_task_date(
                date_start=self.days, date_end=self.days)
        else:
            date_start = self.start_date or self.start_days
            date_end = self.end_date or self.end_days
            tasks._change_project_task_date(
                date_start=date_start, date_end=date_end)

    @api.onchange("days")
    def _onchange_days(self):
        self.ensure_one()
        if self.days:
            self.start_days = 0
            self.end_days = 0
            self.start_date = False
            self.end_date = False

    @api.onchange("start_days")
    def _onchange_start_days(self):
        self.ensure_one()
        if self.start_days:
            self.days = 0
            self.start_date = False

    @api.onchange("end_days")
    def _onchange_end_days(self):
        self.ensure_one()
        if self.end_days:
            self.days = 0
            self.end_date = False

    @api.onchange("start_date")
    def _onchange_start_date(self):
        self.ensure_one()
        if self.start_date:
            self.days = 0
            self.start_days = 0

    @api.onchange("end_date")
    def _onchange_end_date(self):
        self.ensure_one()
        if self.end_date:
            self.days = 0
            self.end_days = 0
