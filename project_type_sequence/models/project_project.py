# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    display_name = fields.Char(
        string="Name",
        automatic=False,
        compute="_compute_display_name",
        store=True,
        precompute=True,
        index=True,
    )

    @api.depends("name", "sequence_code")
    def _compute_display_name(self):
        for project in self:
            project.display_name = _("%(sequence)s - %(name)s") % {
                "sequence": project.sequence_code if project.sequence_code else "",
                "name": project.name if project.name else "",
            }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            type_id = vals.get("type_id")
            if "sequence_code" not in vals and type_id:
                vals = self._search_sequence_code_for_project_type(type_id, vals)
        projects = super().create(vals_list)
        return projects

    def write(self, vals):
        if "type_id" in vals and vals.get("type_id", False):
            vals = self._search_sequence_code_for_project_type(
                vals.get("type_id"), vals
            )
        return super().write(vals)

    def _search_sequence_code_for_project_type(self, type_id, vals):
        project_type = self.env["project.type"].browse(type_id)
        if project_type.sequence_id:
            vals["sequence_code"] = project_type.sequence_id.next_by_id()
        return vals
