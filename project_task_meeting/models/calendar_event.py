# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    task_id = fields.Many2one(
        comodel_name="project.task",
        string="Task",
    )

    task_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Task Customer",
        related="task_id.partner_id",
        store=True,
    )

    @api.model
    def _get_public_fields(self):
        result = super(CalendarEvent, self)._get_public_fields()
        result |= {"task_id"}
        return result
