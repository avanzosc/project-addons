# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.exceptions import AccessError
from odoo.tools.translate import _

from odoo.addons.calendar.models.calendar_event import Meeting


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

    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        groupby = [groupby] if isinstance(groupby, str) else groupby
        grouped_fields = {group_field.split(":")[0] for group_field in groupby}
        private_fields = grouped_fields - self._get_public_fields()
        private_fields.discard("state")
        if not self.env.su and private_fields:
            raise AccessError(
                _(
                    "Grouping by %s is not allowed.",
                    ", ".join(
                        [
                            self._fields[field_name].string
                            for field_name in private_fields
                        ]
                    ),
                )
            )
        return super(Meeting, self).read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )
