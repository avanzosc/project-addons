# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccounAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    vehicle_id = fields.Many2one(
        string="Vehicle", comodel_name="fleet.vehicle", compute="_compute_vehicle_id"
    )

    def _compute_vehicle_id(self):
        for analytic in self:
            analytic.vehicle_id = analytic.account_id.project_ids[:1].vehicle_id
