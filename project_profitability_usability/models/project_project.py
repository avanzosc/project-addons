# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    revenue_invoiced_amount = fields.Monetary(compute="_compute_profitability")
    revenue_to_invoice_amount = fields.Monetary(compute="_compute_profitability")
    cost_invoiced_amount = fields.Monetary(compute="_compute_profitability")
    cost_to_invoice_amount = fields.Monetary(compute="_compute_profitability")
    profitability_done_amount = fields.Monetary(compute="_compute_profitability")
    profitability_pending_amount = fields.Monetary(compute="_compute_profitability")

    def _compute_profitability(self):
        for project in self:
            profitability_items = project._get_profitability_items(False)
            costs = profitability_items["costs"]["total"]
            revenues = profitability_items["revenues"]["total"]
            project.revenue_invoiced_amount = revenues["invoiced"]
            project.revenue_to_invoice_amount = revenues["to_invoice"]
            project.cost_invoiced_amount = costs["billed"]
            project.cost_to_invoice_amount = costs["to_bill"]
            project.profitability_done_amount = revenues["invoiced"] + costs["billed"]
            project.profitability_pending_amount = (
                revenues["to_invoice"] + costs["to_bill"]
            )
