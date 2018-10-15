# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectProjectRisk(models.Model):
    _inherit = 'project.project'

    risk_table_ids = fields.One2many(
        comodel_name='project.risk.table', inverse_name='project_id')
    risk_chance_table_ids = fields.One2many(
        comodel_name='project.risk.chance.table', inverse_name='project_id')
