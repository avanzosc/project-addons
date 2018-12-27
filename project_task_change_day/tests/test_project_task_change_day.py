# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from odoo import fields
str2date = fields.Date.from_string


class TestProjectTaskChangeDay(common.TransactionCase):

    def setUp(self):
        super(TestProjectTaskChangeDay, self).setUp()
        self.wiz_obj = self.env['wiz.change.project.task.date']
        task_vals = {
            'name': 'task TestProjectTaskChangeDay',
            'date_start': "{}-01-01 08:00:00".format(
                str2date(fields.Date.today()).year),
            'date_end': "{}-01-15 20:00:00".format(
                str2date(fields.Date.today()).year)}
        project_vals = {
            'name': 'Project TestProjectTaskChangeDay',
            'task_ids': [(0, 0, task_vals)]}
        self.project = self.env['project.project'].create(project_vals)

    def test_project_task_change_day(self):
        task = self.project.task_ids[0]
        wiz = self.wiz_obj.create({'days': 5})
        wiz.with_context(active_ids=[task.id]).change_project_task_date()
        date_start = "{}-01-06 08:00:00".format(
            str2date(fields.Date.today()).year)
        date_end = "{}-01-20 20:00:00".format(
            str2date(fields.Date.today()).year)
        self.assertEqual(
            task.date_start, date_start, 'BAD date start(1)')
        self.assertEqual(
            task.date_end, date_end, 'BAD date end(1)')
        wiz.days = -2
        wiz.with_context(active_ids=[task.id]).change_project_task_date()
        date_start = "{}-01-04 08:00:00".format(
            str2date(fields.Date.today()).year)
        date_end = "{}-01-18 20:00:00".format(
            str2date(fields.Date.today()).year)
        self.assertEqual(
            task.date_start, date_start, 'BAD date start(2)')
        self.assertEqual(
            task.date_end, date_end, 'BAD date end(2)')
