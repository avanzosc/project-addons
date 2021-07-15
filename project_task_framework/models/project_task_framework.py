# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProjectTaskFramework(models.Model):
    _name = 'project.task.framework'
    _description = 'Framework'

    name = fields.Char(string='Framework', required=True, translate=True)
