# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_funding_account = fields.Boolean(
        string='Funding Account Visible',
        implied_group='project_funding.group_funding_account')
