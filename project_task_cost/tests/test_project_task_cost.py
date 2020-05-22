# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from dateutil.relativedelta import relativedelta
import calendar

from odoo import fields
from odoo.tests import common

str2date = fields.Date.from_string


@common.at_install(False)
@common.post_install(True)
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
        self.project.button_recompute_costs()
        self.assertEquals(task.employee_cost, self.timesheet_cost)
        self.assertEquals(
            task.employee_cost * task.planned_hours, task.planned_cost)
        self.assertEquals(
            task.employee_cost * task.effective_hours, task.effective_cost)
        task.invalidate_cache()
        self.assertEquals(
            task.planned_hours / month_gap, task.planned_monthly_hours)
        calendar_num = (
            str2date(task.date_end) - str2date(task.date_start)).days + 1
        self.assertEquals(len(task.calendar_ids), calendar_num)
        self.assertEquals(
            round(sum(task.mapped('calendar_ids.planned_hours')), 2),
            round(task.planned_hours, 2))
        self.assertEquals(
            round(sum(task.mapped('calendar_ids.planned_cost')), 2),
            round(task.planned_cost, 2))
        self.assertEquals(
            round(sum(task.mapped('calendar_ids.effective_hours')), 2),
            round(task.effective_hours, 2))
        self.assertEquals(
            round(sum(task.mapped('calendar_ids.effective_cost')), 2),
            round(task.effective_cost, 2))
        self.assertFalse(task.timesheet_ids)
        task.write({
            'timesheet_ids': [(0, 0, {
                'date': str2date(task.date_end) + relativedelta(days=10),
                'user_id': task.user_id.id,
                'employee_id': self.employee.id,
                'unit_amount': 10.0,
                'name': 'Timesheet Test',
                'account_id': self.project.analytic_account_id.id,
                'project_id': self.project.id,
            })]
        })
        self.assertTrue(len(task.calendar_ids) > calendar_num)
        task.timesheet_ids.unlink()
        self.assertEquals(len(task.calendar_ids), calendar_num)

    def test_planned_monthly_hours(self):
        today = str2date(fields.Date.today())
        date_start = today.replace(day=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        date_end = today.replace(day=last_day)
        task = self.task_model.create({
            'name': 'Name',
            'planned_hours': 30.0,
            'user_id': self.env.user.id,
            'date_start': date_start,
            'date_end': date_end,
            'project_id': self.project.id,
        })
        self.assertEquals(task.planned_hours, task.planned_monthly_hours)
        date_end = date_start + relativedelta(months=1)
        task.write({
            'date_end': date_end,
        })
        self.assertNotEquals(date_start.month, date_end.month)
        self.assertEquals(task.planned_hours, task.planned_monthly_hours)
        last_day = calendar.monthrange(date_end.year, date_end.month)[1]
        date_end = date_end.replace(day=last_day)
        task.write({
            'date_end': date_end,
        })
        self.assertNotEquals(date_start.month, date_end.month)
        self.assertNotEquals(task.planned_hours, task.planned_monthly_hours)
        self.assertEquals(round(task.planned_hours / 2, 2),
                          task.planned_monthly_hours)
        date_end = date_start + relativedelta(years=1)
        task.write({
            'date_end': date_end,
        })
        self.assertEquals(round(task.planned_hours / 12, 2),
                          task.planned_monthly_hours)
        date_end += relativedelta(days=1)
        date_end = date_end.replace(day=15)
        task.write({
            'date_end': date_end
        })
        self.assertEquals(round(task.planned_hours / 12, 2),
                          task.planned_monthly_hours)
        date_end = date_end.replace(day=16)
        task.write({
            'date_end': date_end,
        })
        self.assertEquals(round(task.planned_hours / 13, 2),
                          task.planned_monthly_hours)
