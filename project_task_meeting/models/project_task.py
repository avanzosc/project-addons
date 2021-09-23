# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, _


class ProjectTack(models.Model):
    _inherit = 'project.task'

    count_calendar_event = fields.Integer(
        string='# Meetings', compute='_compute_count_calendar_event')
    calendar_event_ids = fields.One2many(
        string='Meetings', comodel_name='calendar.event',
        inverse_name='task_id')

    def _compute_count_calendar_event(self):
        for task in self:
            cond = [('task_id', '=', task.id)]
            meetings = self.env['calendar.event'].search(cond)
            task.count_calendar_event = len(meetings)

    def action_to_calendar_event(self):
        context = self.env.context.copy()
        if 'params' in context:
            params = context.get('params', {})
            if 'model' in params and params.get('model', 'a') == 'sale.order':
                context.pop('params')
        context.update({
            'search_default_task_id': self.id,
            'default_task_id': self.id,
            'default_name': self.name,
            'active_model': 'project.task',
            'active_id': self.id,
            'active_ids': self.ids})
        return {
            'name': _('Meetings'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form,calendar',
            'res_model': 'calendar.event',
            'context': context,
            'domain': [('id', 'in', self.calendar_event_ids.ids)],
        }
