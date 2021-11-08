# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    vehicle_id = fields.Many2one(
        string='Vehicle', comodel_name='fleet.vehicle')
