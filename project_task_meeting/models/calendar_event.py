# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models

from odoo.addons.calendar.models.calendar_attendee import Attendee


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    attendee_status = fields.Selection(
        Attendee.STATE_SELECTION,
        string="Attendee Status",
        compute="_compute_attendee",
        store="True",
    )

    task_id = fields.Many2one(
        string="Task",
        comodel_name="project.task",
    )

    task_partner_id = fields.Many2one(
        "res.partner",
        string="Task Customer",
        related="task_id.partner_id",
        store=True,
    )

    @api.model
    def _get_public_fields(self):
        result = super(CalendarEvent, self)._get_public_fields()
        result |= {"task_id"}
        return result
