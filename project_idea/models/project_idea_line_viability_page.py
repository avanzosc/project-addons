# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectLineViabilityPage(models.Model):
    _inherit = 'project.project'

    viability_page = fields.One2many(
        string='Viability', comodel_name='project.idea.line.viability',
        inverse_name='project_id')
