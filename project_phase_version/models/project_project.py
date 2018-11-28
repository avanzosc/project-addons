# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'



class ProjectPhase(models.Model):
    _inherit = 'project.phase'

    new_version = fields.Boolean(string='Create New Version')
    historify = fields.Boolean(string='Historify')
