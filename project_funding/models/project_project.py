# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    funding_ids = fields.One2many(
        comodel_name='funding.source.project', inverse_name='project_id',
        string='Funding Sources')
