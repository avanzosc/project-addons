# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectGoal(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProjectGoal, cls).setUpClass()
        cls.project = cls.env['project.project'].create({
            'name': 'New Project',
            'goal_ids': [
                (0, 0, {'name': 'Goal 1'}),
                (0, 0, {'name': 'Goal 2'}),
            ]
        })

    def test_project_disable_enable(self):
        self.assertTrue(self.project.active)
        for goal in self.project.with_context(active_test=False).goal_ids:
            self.assertTrue(goal.active)
        self.project.toggle_active()
        self.assertFalse(self.project.active)
        for goal in self.project.with_context(active_test=False).goal_ids:
            self.assertFalse(goal.active)
        self.project.toggle_active()
        self.assertTrue(self.project.active)
        for goal in self.project.with_context(active_test=False).goal_ids:
            self.assertTrue(goal.active)
