# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common
from odoo import fields
str2date = fields.Date.from_string


@common.at_install(False)
@common.post_install(True)
class TestProjectUtilities(common.TransactionCase):

    def setUp(self):
        super(TestProjectUtilities, self).setUp()
        self.wiz_obj = self.env['wiz.change.project.task.date']
        self.current_year = str2date(fields.Date.today()).year
        task_vals = {
            'name': 'task for test project_utilities',
            'date_start': "{}-01-01 08:00:00".format(self.current_year),
            'date_end': "{}-01-15 20:00:00".format(self.current_year)}
        project_vals = {
            'name': 'Project for test project_utilities',
            'task_ids': [(0, 0, task_vals)]}
        self.project = self.env['project.project'].create(project_vals)

    def test_show_analytic_account(self):
        result = self.project.show_analytic_account_from_project()
        domain = result.get('domain')
        self.assertEquals(domain,
                          [('id', '=', self.project.analytic_account_id.id)])

    def test_project_task_change_days_parameter(self):
        task = self.project.task_ids[:1]
        wiz = self.wiz_obj.with_context(active_ids=[task.id]).create({
            "days": 5,
            "start_days": 2,
            "end_days": 2,
            "start_date": "{}-02-01 08:00:00".format(self.current_year),
            "end_date": "{}-02-15 08:00:00".format(self.current_year),
        })
        wiz.button_change_project_task_date()
        date_start = "{}-01-06 08:00:00".format(self.current_year)
        date_end = "{}-01-20 20:00:00".format(self.current_year)
        self.assertEqual(
            task.date_start, date_start, "Wrong date start")
        self.assertEqual(
            task.date_end, date_end, "Wrong date end")
        wiz.days = -2
        wiz.button_change_project_task_date()
        date_start = "{}-01-04 08:00:00".format(self.current_year)
        date_end = "{}-01-18 20:00:00".format(self.current_year)
        self.assertEqual(
            task.date_start, date_start, "Wrong date start")
        self.assertEqual(
            task.date_end, date_end, "Wrong date end")

    def test_project_task_change_different_days(self):
        task = self.project.task_ids[:1]
        wiz = self.wiz_obj.with_context(active_ids=[task.id]).create({
            "days": 0,
            "start_days": 6,
            "end_days": 4,
        })
        wiz.button_change_project_task_date()
        date_start = "{}-01-07 08:00:00".format(self.current_year)
        date_end = "{}-01-19 20:00:00".format(self.current_year)
        self.assertEqual(
            task.date_start, date_start, "Wrong date start")
        self.assertEqual(
            task.date_end, date_end, "Wrong date end")
        wiz.write({
            "start_days": -3,
            "end_days": -1,
        })
        wiz.button_change_project_task_date()
        date_start = "{}-01-04 08:00:00".format(self.current_year)
        date_end = "{}-01-18 20:00:00".format(self.current_year)
        self.assertEqual(
            task.date_start, date_start, "Wrong date start")
        self.assertEqual(
            task.date_end, date_end, "Wrong date end")

    def test_project_task_change_dates(self):
        task = self.project.task_ids[:1]
        date_start = "{}-01-06 08:00:00".format(self.current_year)
        date_end = "{}-01-20 20:00:00".format(self.current_year)
        wiz = self.wiz_obj.with_context(active_ids=[task.id]).create({
            "days": 0,
            "start_days": 0,
            "end_days": 0,
            "start_date": date_start,
            "end_date": date_end,
        })
        wiz.button_change_project_task_date()
        self.assertEqual(
            task.date_start, date_start, "Wrong date start")
        self.assertEqual(
            task.date_end, date_end, "Wrong date end")

    def test_project_task_change_mixed(self):
        task = self.project.task_ids[:1]
        date_end = "{}-01-20 20:00:00".format(self.current_year)
        wiz = self.wiz_obj.with_context(active_ids=[task.id]).create({
            "days": 0,
            "start_days": 2,
            "end_date": date_end,
        })
        wiz.button_change_project_task_date()
        new_date_start = "{}-01-03 08:00:00".format(self.current_year)
        self.assertEqual(
            task.date_start, new_date_start, "Wrong date start")
        self.assertEqual(
            task.date_end, date_end, "Wrong date end")
        change_date_start = "{}-01-06 08:00:00".format(self.current_year)
        wiz.write({
            "start_days": 0,
            "end_days": -1,
            "start_date": change_date_start,
            "end_date": False,
        })
        wiz.button_change_project_task_date()
        new_date_end = "{}-01-19 20:00:00".format(self.current_year)
        self.assertEqual(
            task.date_start, change_date_start, "Wrong date start")
        self.assertEqual(
            task.date_end, new_date_end, "Wrong date end")

    def test_wizard_onchanges(self):
        task = self.project.task_ids[:1]
        wiz = self.wiz_obj.with_context(active_ids=[task.id]).create({
            "days": 5,
        })
        self.assertEquals(wiz.days, 5)
        self.assertEquals(wiz.start_days, 0)
        self.assertEquals(wiz.end_days, 0)
        self.assertEquals(wiz.start_date, False)
        self.assertEquals(wiz.end_date, False)
        wiz.start_days = 2
        wiz._onchange_start_days()
        self.assertEquals(wiz.days, 0)
        self.assertEquals(wiz.start_days, 2)
        self.assertEquals(wiz.end_days, 0)
        self.assertEquals(wiz.start_date, False)
        self.assertEquals(wiz.end_date, False)
        wiz.end_days = 2
        wiz._onchange_end_days()
        self.assertEquals(wiz.days, 0)
        self.assertEquals(wiz.start_days, 2)
        self.assertEquals(wiz.end_days, 2)
        self.assertEquals(wiz.start_date, False)
        self.assertEquals(wiz.end_date, False)
        wiz.start_date = task.date_start
        wiz._onchange_start_date()
        self.assertEquals(wiz.days, 0)
        self.assertEquals(wiz.start_days, 0)
        self.assertEquals(wiz.end_days, 2)
        self.assertEquals(wiz.start_date, task.date_start)
        self.assertEquals(wiz.end_date, False)
        wiz.end_date = task.date_end
        wiz._onchange_end_date()
        self.assertEquals(wiz.days, 0)
        self.assertEquals(wiz.start_days, 0)
        self.assertEquals(wiz.end_days, 0)
        self.assertEquals(wiz.start_date, task.date_start)
        self.assertEquals(wiz.end_date, task.date_end)
        wiz.days = 5
        wiz._onchange_days()
        self.assertEquals(wiz.days, 5)
        self.assertEquals(wiz.start_days, 0)
        self.assertEquals(wiz.end_days, 0)
        self.assertEquals(wiz.start_date, False)
        self.assertEquals(wiz.end_date, False)
