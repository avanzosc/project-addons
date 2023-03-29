# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestProjectGoal(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProjectGoal, cls).setUpClass()
        goal_type = cls.env.ref("project_goal.gtype1")
        cls.goal_type2 = cls.env.ref("project_goal.gtype2")
        cls.goal = cls.env["project.goal.goal"].create(
            {
                "name": "New Goal",
                "description": "Goal Description",
                "type_id": goal_type.id,
            }
        )
        cls.project = cls.env["project.project"].create(
            {
                "name": "New Project",
                "goal_ids": [
                    (0, 0, {"name": "Goal 1", "type_id": goal_type.id}),
                    (0, 0, {"name": "Goal 2", "type_id": goal_type.id}),
                ],
            }
        )

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

    def test_project_goal_onchanges(self):
        for goal in self.project.with_context(active_test=False).goal_ids:
            self.assertFalse(goal.goal_id)
            self.assertNotEquals(goal.name, self.goal.description)
            goal.write(
                {
                    "goal_id": self.goal.id,
                }
            )
            goal.onchange_goal_id()
            self.assertEquals(goal.name, self.goal.description)
            goal.write(
                {
                    "type_id": self.goal_type2.id,
                }
            )
            goal.onchange_type_id()
            self.assertFalse(goal.goal_id)
