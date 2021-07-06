# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    task_id = fields.Many2one(
        string='Task', comodel_name='project.task')

    @api.model
    def _get_public_fields(self):
        result = super(CalendarEvent, self)._get_public_fields()
        result |= {'task_id'}
        return result
