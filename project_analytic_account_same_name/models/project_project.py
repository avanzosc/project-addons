# Copyright 2022 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.multi
    def write(self, vals):
        result = super(ProjectProject, self).write(vals)
        if 'name' in vals and vals.get('name', False):
            for project in self.filtered(lambda x: x.analytic_account_id):
                if len(project.analytic_account_id.project_ids) == 1:
                    project.analytic_account_id.name = project.name
        return result
