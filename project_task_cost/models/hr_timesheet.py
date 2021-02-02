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
    def write(self, vals):
        res = super(HrTimesheet, self).write(vals)
        if 'date' or 'unit_amount' or 'task_id' in vals:
            self.filtered("task_id").create_calendar()
        return res

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
                     line.date > line.task_id.date_end) or
                    (line.task_id.date_start and
                     line.date < line.task_id.date_start))):
                calendars = calendar_obj.search([
                    ('task_id', '=', line.task_id.id),
                    ('date', '=', line.date),
                ])
                calendars.unlink()
        return super(HrTimesheet, self).unlink()

    @api.multi
    def create_calendar(self):
        for task in self.mapped("task_id"):
            lines = self.filtered(
                lambda l: l.task_id == task and
                (l.date < task.date_start or l.date > task.date_end)
                and l.date not in task.mapped("calendar_ids.date"))
            task.write({
                "calendar_ids": [(0, 0, {
                    "date": x,
                    "task_id": task.id}) for x in lines.mapped("date")],
            })
