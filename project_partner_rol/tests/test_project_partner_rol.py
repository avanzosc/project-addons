# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests.common import SavepointCase
from odoo import fields
from odoo.exceptions import ValidationError

from dateutil import relativedelta


class TestProjectPartnerRol(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProjectPartnerRol, cls).setUpClass()
        cls.month_number = 5
        cls.today = fields.Datetime.from_string(fields.Datetime.now())
        cls.delta = relativedelta.relativedelta(months=+cls.month_number)
        cls.taskdelta = relativedelta.relativedelta(
            months=+2 * cls.month_number)
        cls.project = cls.env['project.project'].create({
            'name': 'Test Project',
            'participant_ids': [
                (0, 0, {'partner_id': cls.env.user.partner_id.id,
                        'planned_hours_percentage': 100.0})],
            'planned_date_start': cls.today,
            'planned_date_end': cls.today + cls.delta,
            'planned_hours': 25.0,
        })

    def test_project_data(self):
        self.assertFalse(self.project.task_ids)
        self.assertFalse(self.project.task_planned_hours)
        self.assertFalse(self.project.task_date_start)
        self.assertFalse(self.project.task_date_end)
        self.assertFalse(self.project.task_date_margin)
        self.assertEquals(self.project.planned_date_margin, self.month_number)
        for participant in self.project.participant_ids:
            self.assertFalse(participant.task_planned_hours)
            self.assertFalse(participant.monthly_task_planned_hours)
            self.assertEquals(
                participant.project_planned_hours,
                (participant.project_id.planned_hours *
                 (participant.planned_hours_percentage / 100.0)))

    def test_project_task_data(self):
        task = self.project.task_ids.create({
            'project_id': self.project.id,
            'name': 'Test Task',
            'date_start': self.today,
            'date_end': self.today + self.taskdelta,
            'planned_hours': 20.0,
        })
        self.assertTrue(self.project.task_ids)
        self.assertEquals(self.project.task_date_start, task.date_start)
        self.assertEquals(self.project.task_date_end, task.date_end)
        self.assertEquals(
            self.project.task_date_margin, 2 * self.month_number)
        self.assertEquals(self.project.task_planned_hours, task.planned_hours)
        for participant in self.project.participant_ids:
            self.assertEquals(
                participant.project_planned_hours,
                (participant.project_id.planned_hours *
                 (participant.planned_hours_percentage / 100.0)))
            self.assertEquals(
                participant.monthly_planned_hours,
                (participant.project_planned_hours /
                 participant.project_id.planned_date_margin))
            self.assertEquals(
                participant.task_planned_hours,
                (participant.project_id.task_planned_hours *
                 (participant.planned_hours_percentage / 100.0)))
            self.assertEquals(
                participant.monthly_task_planned_hours,
                (participant.task_planned_hours /
                 participant.project_id.task_date_margin))

    def test_participant_percentage_constraint(self):
        participant = self.project.participant_ids[:1]
        with self.assertRaises(ValidationError):
            participant.write({
                'planned_hours_percentage': -0.1,
            })
        with self.assertRaises(ValidationError):
            participant.write({
                'planned_hours_percentage': 100.1,
            })
        participant.write({
            'planned_hours_percentage': 0.0,
        })

    def test_start_end_same_date(self):
        self.project.write({
            'planned_date_end': self.project.planned_date_start,
        })
        self.assertFalse(self.project.planned_date_margin)
