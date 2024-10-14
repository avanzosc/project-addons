# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.model_create_multi
    def create(self, vals_list):
        context = self.env.context
        ProjectType = self.env["project.type"]
        for vals in vals_list:
            if "name" in vals and "from_sale_line" not in context:
                vals.pop("name")
            type_id = vals.get("type_id")
            if "sequence_code" not in vals and type_id:
                project_type = ProjectType.browse(type_id)
                if project_type.sequence_id:
                    sequence_code = project_type.sequence_id.next_by_id()
                    vals["sequence_code"] = sequence_code
                    if "name" in vals and "from_sale_line" in context:
                        vals["name"] = f"{sequence_code} - {vals['name']}"
        projects = super().create(vals_list)
        if "from_sale_line" in context:
            for project in projects:
                if project.sequence_code and project.sequence_code not in project.name:
                    project.name = f"{project.sequence_code} - {project.name}"
        return projects
