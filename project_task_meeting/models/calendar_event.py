# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

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

    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        groupby = [groupby] if isinstance(groupby, str) else groupby
        groupby = [field for field in groupby if field.split(":")[0] != "state"]
        return super(CalendarEvent, self).read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )
