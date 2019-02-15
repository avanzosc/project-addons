# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from dateutil.relativedelta import relativedelta

from odoo import exceptions, fields
from odoo.tests import common

str2date = fields.Date.from_string


class TestProjectTaskCost(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProjectTaskCost, cls).setUpClass()
        cls.task_model = cls.env['project.task']
        employee_model = cls.env['hr.employee']
        cls.project = cls.env['project.project'].create({
            'name': 'Test Project',
        })
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
        date_start = str2date(fields.Datetime.now()) + relativedelta(days=1)
        date_end = date_start + relativedelta(months=month_gap)
        task = self.task_model.create({
            'name': 'Name',
            'planned_hours': 30.0,
            'user_id': self.env.user.id,
            'date_start': date_start,
            'date_end': date_end,
            'project_id': self.project.id,
        })
        datedelta = relativedelta(
            str2date(task.date_end), str2date(task.date_start))
        month_gap = (datedelta.years * 12) + datedelta.months
        self.assertFalse(task.employee_cost)
        task._onchange_user()
        self.assertEquals(task.employee_cost, self.timesheet_cost)
        self.assertEquals(
            task.employee_cost * task.planned_hours, task.planned_cost)
        self.assertEquals(
            task.employee_cost * task.effective_hours, task.effective_cost)
        task.invalidate_cache()
        self.assertEquals(
            task.planned_hours / (month_gap + 1), task.planned_monthly_hours)
        self.assertFalse(task.calendar_ids)
        self.project.button_create_task_calendar()
        calendar_num = (
            str2date(task.date_end) - str2date(task.date_start)).days + 1
        self.assertEquals(len(task.calendar_ids), calendar_num)
        with self.assertRaises(exceptions.ValidationError):
            task.calendar_ids.create({
                'task_id': task.id,
                'date': date_start - relativedelta(days=10),
            })
        with self.assertRaises(exceptions.ValidationError):
            task.calendar_ids.create({
                'task_id': task.id,
                'date': date_end + relativedelta(days=10),
            })
