# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_disable_html = fields.Boolean(
        string='Disable HTML Tasks Descriptions',
        implied_group='project_utilities.disable_html_task_description')
    group_visible_task_period = fields.Boolean(
        string='Task Period Visible in List View',
        implied_group='project_utilities.visible_task_period')
    group_visible_task_period_date = fields.Boolean(
        string='Task Period Visible in List View (date only)',
        implied_group='project_utilities.visible_task_period_date')
