# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectTaskShortcut(models.Model):
    _inherit = 'project.project'
    _description = 'Tasks Shortcut'

    task_count = fields.Integer(
        string='Tasks', compute='_task_count')

    @api.multi
    def _task_count(self):
        task_obj = self.env['project.task']
        for project in self:
            project.task_count = task_obj.search_count([(
                'project_id', '=', project.id)])
