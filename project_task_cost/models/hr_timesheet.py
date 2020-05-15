# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class HrTimesheet(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def create(self, vals):
        line = super(HrTimesheet, self).create(vals)
        if 'task_id' in vals:
            line.create_calendar()
        return line

    @api.multi
    def unlink(self):
        calendar_obj = self.sudo().env['project.task.calendar']
        for line in self.filtered('task_id'):
            timesheets = self.search([
                ('task_id', '=', line.task_id.id),
                ('date', '=', line.date),
                ('id', 'not in', self.ids),
            ])
            if (not timesheets and (
                    (line.task_id.date_end and
                     line.date > line.task_id.date_end.date()) or
                    (line.task_id.date_start and
                     line.date < line.task_id.date_start.date()))):
                calendars = calendar_obj.search([
                    ('task_id', '=', line.task_id.id),
                    ('date', '=', line.date),
                ])
                calendars.unlink()
        return super(HrTimesheet, self).unlink()

    @api.multi
    def create_calendar(self):
        calendar_obj = self.sudo().env['project.task.calendar']
        for line in self.filtered('task_id'):
            calendar = calendar_obj.search([
                ('task_id', '=', line.task_id.id),
                ('date', '=', line.date),
            ])
            if not calendar:
                calendar_obj.create({
                    'task_id': line.task_id.id,
                    'date': line.date,
                })
