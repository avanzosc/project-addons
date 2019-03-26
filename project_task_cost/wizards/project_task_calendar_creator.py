# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProjectTaskCalendarCreator(models.TransientModel):
    _name = 'project.task.calendar.creator'
    _description = 'Wizard to Create Task Calendars'

    @api.multi
    def button_create_calendar(self):
        task_obj = self.env['project.task']
        domain = []
        if not self.env.context.get('all'):
            domain = [('calendar_ids', '=', [])]
        tasks = task_obj.search(domain)
        tasks.button_create_calendar()
        return self.button_open_calendar()

    @api.multi
    def button_open_calendar(self):
        action = self.env.ref('project_task_cost.project_task_calendar_action')
        return action.read()[0]
