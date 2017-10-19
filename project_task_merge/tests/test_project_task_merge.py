# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProjectTaskMerge(common.TransactionCase):

    def setUp(self):
        super(TestProjectTaskMerge, self).setUp()
        self.project_model = self.env['project.project']
        self.wiz_model = self.env['wiz.project.task.merge']
        task_types = self.env['project.task.type'].search([])
        self.task_type = min(task_types, key=lambda x: x.sequence)
        project_vals = {'name': 'Project task merge 1',
                        'use_tasks': True}
        task_vals = {'name': 'Project task merge 1 - task 1',
                     'date_start': '2017-01-08 15:00:00',
                     'planned_hours': 5.0,
                     'work_ids': [(0, 0, {'name': 'task1 - inputation 1',
                                          'hours': 5.0})]}
        task_vals2 = {'name': 'Project task merge 1 - task 2',
                      'date_start': '2017-01-01 15:00:00',
                      'date_deadline': '2017-06-15',
                      'planned_hours': 15.0,
                      'work_ids': [(0, 0, {'name': 'task1 - inputation 2',
                                           'hours': 15.0})]}
        project_vals['tasks'] = [(0, 0, task_vals), (0, 0, task_vals2)]
        self.project1 = self.project_model.create(project_vals)

    def test_project_task_merge(self):
        wiz = self.wiz_model.create({})
        wiz.with_context({'active_ids': self.project1.tasks.ids}).merge_tasks()
        task = self.project1.mapped('tasks').filtered(
            lambda x: x.stage_id.id ==
            self.env.ref('project.project_tt_cancel').id)
        self.assertEqual(
            len(task), 1, 'Canceled task not found.')
        task = self.project1.mapped('tasks').filtered(
            lambda x: x.stage_id.id == self.task_type.id)
        self.assertEqual(
            len(task), 1, 'Task not found with analysis state.')
        self.assertEqual(
            task.planned_hours, 20.00, 'Bad planned hour in task.')
        self.assertEqual(
            task.date_start, '2017-01-01 15:00:00', 'Bad date start in task.')
        self.assertEqual(
            task.date_deadline, '2017-06-15', 'Bad date dead line in task.')
