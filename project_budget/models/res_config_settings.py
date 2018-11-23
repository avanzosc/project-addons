# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_smartbutton_actual_budget = fields.Boolean(
        string='Smartbutton To Current Month Budget',
        implied_group='project_budget.smartbutton_actual_budget')
