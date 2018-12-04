# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import common


class TestProjectTaskCost(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProjectTaskCost, cls).setUpClass()
        cls.task_model = cls.env['project.task']
        employee_model = cls.env['hr.employee']
        cls.employee = employee_model.search([
            ('user_id', '=', cls.env.user.id)], limit=1)
        if not cls.employee:
            cls.employee = employee_model.create({
                'name': cls.env.user.name,
                'user_id': cls.env.user.id,
            })
        cls.timesheet_cost = 20.0
        cls.employee.timesheet_cost = cls.timesheet_cost

    def test_task_create(self):
        month_gap = 2
        date_start = fields.Datetime.from_string(fields.Datetime.now())
        date_end = date_start + relativedelta(months=month_gap)
        task = self.task_model.create({
            'name': 'Name',
            'planned_hours': 30.0,
            'user_id': self.env.user.id,
            'date_start': date_start,
            'date_end': date_end,
        })
        self.assertFalse(task.employee_cost)
        task._onchange_user()
        self.assertEquals(task.employee_cost, self.timesheet_cost)
        self.assertEquals(
            task.employee_cost * task.planned_hours, task.planned_cost)
        self.assertEquals(
            task.employee_cost * task.effective_hours, task.effective_cost)
        self.assertEquals(
            task.planned_hours / (month_gap + 1), task.planned_monthly_hours)
