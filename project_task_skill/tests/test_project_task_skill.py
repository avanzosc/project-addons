# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests.common import SavepointCase


class TestProjectTaskSkill(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProjectTaskSkill, cls).setUpClass()
        employee_model = cls.env['hr.employee']
        skill_model = cls.env['hr.skill']
        task_model = cls.env['project.task']
        cls.skill = skill_model.create({
            'name': 'Parent Skill',
            'child_ids': [(0, 0, {'name': 'Child Skill'})],
        })
        cls.skill2 = skill_model.create({
            'name': 'Parent Skill 2',
            'child_ids': [(0, 0, {'name': 'Child Skill 2'})],
        })
        cls.employee = cls.env.user.employee_ids[:1] or employee_model.create({
            'name': 'New Employee',
            'user_id': cls.env.user.id,
        })
        cls.employee.write({
            'employee_skill_ids': [
                (0, 0, {'skill_id': cls.skill.child_ids[:1].id,
                        'level': '2'}),
                (0, 0, {'skill_id': cls.skill2.child_ids[:1].id,
                        'level': '0'})]
        })
        cls.task = task_model.create({
            'name': 'New Task',
            'parent_skill_id': cls.skill2.id,
            'skill_id': cls.skill2.child_ids[:1].id,
            'skill_level': '0',
            'user_id': cls.env.user.id,
        })

    def test_project_task_skill(self):
        self.assertIn(self.employee.user_id, self.task.possible_user_ids)
        self.task.write({
            'parent_skill_id': self.skill.id,
        })
        self.task._onchange_parent_skill_id()
        self.assertFalse(self.task.skill_id)
        self.assertEquals(self.task.skill_level, '0')
        self.assertNotIn(self.employee.user_id, self.task.possible_user_ids)
        self.task._onchange_skill_and_level()
        self.assertFalse(self.task.user_id)
        self.task.write({
            'skill_id': self.skill.child_ids[:1].id,
        })
        self.assertNotIn(self.employee.user_id, self.task.possible_user_ids)
        self.task.write({
            'skill_level': '2',
        })
        self.assertIn(self.employee.user_id, self.task.possible_user_ids)
