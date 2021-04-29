# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    allowed_project_user_ids = fields.Many2many(
        comodel_name="res.users", string="Allowed Project Managers",
        compute="_compute_allowed_project_user_ids", store=True)

    @api.depends("order_line", "order_line.account_analytic_id",
                 "order_line.account_analytic_id.project_ids",
                 "order_line.account_analytic_id.project_ids.user_id")
    def _compute_allowed_project_user_ids(self):
        for order in self:
            project_managers = order.mapped(
                "order_line.account_analytic_id.project_ids.user_id")
            order.allowed_project_user_ids = [(6, 0, project_managers.ids)]
