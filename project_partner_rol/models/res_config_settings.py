# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_planned_hours_project = fields.Boolean(
        string="Planned Hours",
        implied_group="project_partner_rol.group_planned_hours_project")
