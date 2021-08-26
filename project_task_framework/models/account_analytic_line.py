# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    framework_id = fields.Many2one(
        string='Framework', comodel_name='project.task.framework',
        related='task_id.framework_id', store=True)
    generic = fields.Boolean(
        string='Is generic?', related='task_id.generic', store=True)
    project_type_id = fields.Many2one(
        string='Project type', comodel_name='project.type',
        related='task_id.type_id', store=True)
