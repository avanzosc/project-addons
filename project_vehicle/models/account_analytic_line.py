# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccounAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    vehicle_id = fields.Many2one(
        string="Vehicle",
        comodel_name="fleet.vehicle",
        related="account_id.vehicle_id",
        store=True,
    )
