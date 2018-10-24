# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectTaskMilestonePhase(models.Model):
    _inherit = 'project.project'

    phase_table_ids = fields.One2many(
        comodel_name='project.task.phase.table', inverse_name='project_id')
