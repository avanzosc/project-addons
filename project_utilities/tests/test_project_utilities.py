# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common
from odoo import fields
str2date = fields.Date.from_string


class TestProjectUtilities(common.TransactionCase):

    def setUp(self):
        super(TestProjectUtilities, self).setUp()
        self.wiz_obj = self.env['wiz.change.project.task.date']
        task_vals = {
            'name': 'task for test project_utilities',
            'date_start': "{}-01-01 08:00:00".format(
                str2date(fields.Date.today()).year),
            'date_end': "{}-01-15 20:00:00".format(
                str2date(fields.Date.today()).year)}
        project_vals = {
            'name': 'Project for test project_utilities',
            'task_ids': [(0, 0, task_vals)]}
        self.project = self.env['project.project'].create(project_vals)

    def test_show_analytic_account(self):
        result = self.project.show_analytic_account_from_project()
        domain = result.get('domain')
        self.assertEquals(domain,
                          [('id', '=', self.project.analytic_account_id.id)])

    def test_project_task_change_day(self):
        task = self.project.task_ids[0]
        wiz = self.wiz_obj.with_context(active_ids=[task.id]).create({
            'days': 5,
        })
        wiz.button_change_project_task_date()
        date_start = "{}-01-06 08:00:00".format(
            str2date(fields.Date.today()).year)
        date_end = "{}-01-20 20:00:00".format(
            str2date(fields.Date.today()).year)
        self.assertEqual(
            task.date_start, date_start, 'BAD date start(1)')
        self.assertEqual(
            task.date_end, date_end, 'BAD date end(1)')
        wiz.days = -2
        wiz.button_change_project_task_date()
        date_start = "{}-01-04 08:00:00".format(
            str2date(fields.Date.today()).year)
        date_end = "{}-01-18 20:00:00".format(
            str2date(fields.Date.today()).year)
        self.assertEqual(
            task.date_start, date_start, 'BAD date start(2)')
        self.assertEqual(
            task.date_end, date_end, 'BAD date end(2)')
        task._change_project_task_date(0)
        self.assertEqual(task.date_start, date_start)
        self.assertEqual(task.date_end, date_end)
