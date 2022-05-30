# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    partner_shipping_id = fields.Many2one(
        string="Delivery Address",
        comodel_name="res.partner",
        related="project_id.partner_shipping_id",
        store=True,
    )
