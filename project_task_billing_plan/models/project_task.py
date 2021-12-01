# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ProjectTask(models.Model):
    _inherit = "project.task"

    billing_plan_count = fields.Integer(
        string="# Billing Plans", compute="_compute_billing_plan_count")

    @api.multi
    def _compute_billing_plan_count(self):
        plan_obj = self.env["account.analytic.billing.plan"]
        for task in self:
            task.billing_plan_count = plan_obj.search_count(
                [("task_id", "=", task.id)])

    @api.multi
    def button_open_billing_plan(self):
        self.ensure_one()
        action = self.env.ref(
            "account_analytic_billing_plan."
            "action_account_analytic_billing_plan")
        action_dict = action.read()[0] if action else {}
        action_dict["context"] = safe_eval(
            action_dict.get("context", "{}"))
        action_dict["context"].update(
            {"default_analytic_account_id": self.project_id.analytic_account_id.id,
             "default_task_id": self.id,
             "search_default_no_invoiced": True})
        domain = expression.AND([
            [("task_id", "=", self.id)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict
