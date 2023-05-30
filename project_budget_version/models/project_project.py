# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.multi
    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        new = super(ProjectProject, self).copy(default=default)
        if self.env.context.get("historify"):
            for budget in self.budget_ids:
                budget.copy(default={
                    "project_id": new.id,
                    "active": new.active,
                })
        return new

    @api.multi
    def create_initial_project_budget(self, date=False):
        if not self.env.context.get("historify"):
            super(ProjectProject, self).create_initial_project_budget(date=date)
