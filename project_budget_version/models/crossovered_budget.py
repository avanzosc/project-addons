# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class CrossoveredBudget(models.Model):
    _inherit = "crossovered.budget"

    @api.multi
    @api.returns(None, lambda value: value[0])
    def copy_data(self, default=None):
        self.ensure_one()
        default = default or {}
        budget = (
            self.with_context(default_project_id=default.get("project_id")) if
            "project_id" in default else self)
        vals = super(CrossoveredBudget, budget).copy_data(default=default)
        return vals


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    @api.multi
    @api.returns(None, lambda value: value[0])
    def copy_data(self, default=None):
        self.ensure_one()
        default = default or {}
        default_project_id = self.env.context.get("default_project_id")
        if default_project_id:
            default.update({
                "analytic_account_id": self.env["project.project"].browse(
                    default_project_id).analytic_account_id.id
            })
        vals = super(CrossoveredBudgetLines, self).copy_data(default=default)
        return vals
