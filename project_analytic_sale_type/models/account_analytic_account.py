# Copyright (c) 2022 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    sale_type_id = fields.Many2one(
        string="Sale type",
        comodel_name="sale.order.type",
        compute="_compute_sale_type_id",
        store=True,
        copy=False,
    )

    @api.depends("project_ids", "project_ids.sale_type_id")
    def _compute_sale_type_id(self):
        for account in self:
            if account.project_ids and account.project_ids[0].sale_type_id:
                account.sale_type_id = account.project_ids[0].sale_type_id.id
