# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticBillingPlan(models.Model):
    _inherit = "account.analytic.billing.plan"

    allowed_task_ids = fields.Many2many(
        comodel_name="project.task",
        compute="_compute_allowed_task_ids",
        store=True)
    task_id = fields.Many2one(comodel_name="project.task")

    @api.depends("analytic_account_id",
                 "analytic_account_id.project_ids",
                 "analytic_account_id.project_ids.task_ids")
    def _compute_allowed_task_ids(self):
        for line in self:
            line.allowed_task_ids = [
                (6, 0, line.mapped(
                    "analytic_account_id.project_ids.task_ids").ids)]

    @api.onchange("account_analytic_id")
    def onchange_account_analytic_id(self):
        for line in self:
            if line.task_id not in line.allowed_task_ids:
                line.task_id = False
            elif len(line.allowed_task_ids) == 1:
                line.task_id = line.allowed_task_ids[:1]

    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Prepare the dict of values to create the new invoice line for a billing
        plan.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = super(AccountAnalyticBillingPlan, self)._prepare_invoice_line(qty)
        res.update({
            "task_id": self.task_id.id,
        })
        return res
