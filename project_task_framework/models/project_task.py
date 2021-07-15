# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    framework_id = fields.Many2one(
        string='Framework', comodel_name='project.task.framework')
    generic = fields.Boolean(string='Is generic?', default=False)
