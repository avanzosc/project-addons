# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def _merge_tasks_from_wizard(self):
        projects = self.mapped('project_id')
        for project in projects:
            tasks = self.filtered(lambda x: x.project_id.id == project.id)
            tasks._merge_tasks()

    def _merge_tasks(self):
        min_task = min(self, key=lambda x: x.id)
        name = min_task.name
        description = u'{}: {}'.format(min_task.name, min_task.description)
        for task in self.filtered(lambda x: x.id != min_task.id):
            name += u' & {}'.format(task.name)
            description += u'\n{}: {}'.format(task.name, task.description)
            task.stage_id = self.env.ref('project.project_tt_cancel').id
        task_min_date_start = min(self, key=lambda x: x.date_start)
        categs = self.mapped('categ_ids')
        vals = {'name': name,
                'description': description,
                'reviewer_id': min_task.project_id.user_id.id,
                'date_start': task_min_date_start.date_start,
                'date_end': False,
                'date_last_stage_update': fields.Datetime.now(),
                'planned_hours': sum(self.mapped('planned_hours')),
                'stage_id': self.env.ref('project.project_tt_analysis').id,
                'categ_ids': [(6, 0, categs.ids)] if categs else [(6, 0, [])]}
        deadline_tasks = self.filtered(lambda x: x.date_deadline)
        if deadline_tasks:
            vals['date_deadline'] = min(
                deadline_tasks, key=lambda x: x.date_deadline).date_deadline
        min_task.write(vals)
        self.mapped('work_ids').write({'task_id': min_task.id})
