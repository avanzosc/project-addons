# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProjectTaskWorkEstimatedtime(common.TransactionCase):

    def setUp(self):
        super(TestProjectTaskWorkEstimatedtime, self).setUp()
        task_vals = {'name': 'Project task estimated time',
                     'description': 'This is the description'}
        work_vals = {'name': 'Project task work 1',
                     'estimated_time': 5.00,
                     'hours': 6.00}
        task_vals['work_ids'] = [(0, 0, work_vals)]
        self.task = self.env['project.task'].create(task_vals)

    def test_project_task_work_estimated_time(self):
        new_task = self.task.copy()
        self.assertEquals(new_task.description, 'This is the description')
        self.assertEquals(len(new_task.work_ids), 1)
        self.assertEquals(new_task.work_ids[0].name, 'Project task work 1')
        self.assertEquals(new_task.work_ids[0].estimated_time, 5.0)
        self.assertEquals(new_task.work_ids[0].hours, 0.0)
