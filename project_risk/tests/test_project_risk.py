# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectRisk(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProjectRisk, cls).setUpClass()
        cls.table_model = cls.env['project.risk.table']
        cls.chance_model = cls.env['project.risk.chance.table']
        cls.probability = cls.env.ref('project_risk.probab1')
        cls.impact = cls.env.ref('project_risk.impact1')
        cls.chance_prob = cls.env.ref('project_risk.prob1')
        cls.chance_prof = cls.env.ref('project_risk.prof1')
        cls.project = cls.env['project.project'].create({
            'name': 'Test Project',
        })
        cls.risk = cls.env['project.risk.risk'].create({
            'name': 'Test Risk',
        })
        cls.action = cls.env['project.risk.action'].create({
            'name': 'Test Action',
        })
        cls.chance = cls.env['project.risk.chance.project'].create({
            'name': 'Test Chance',
        })

    def test_risk_table(self):
        table = self.table_model.create({
            'project_id': self.project.id,
        })
        self.assertFalse(table.risk_level)
        table.write({
            'probability_id': self.probability.id,
            'impact_id': False,
        })
        self.assertFalse(table.risk_level)
        table.write({
            'probability_id': False,
            'impact_id': self.impact.id,
        })
        self.assertFalse(table.risk_level)
        table.write({
            'probability_id': self.probability.id,
            'impact_id': self.impact.id,
        })
        self.assertTrue(table.risk_level)
        self.assertEquals(
            round(table.risk_level, 4),
            round(self.impact.rating * self.probability.rating, 4))

    def test_chance_table(self):
        table = self.chance_model.create({
            'project_id': self.project.id,
        })
        self.assertFalse(table.chance_level)
        table.write({
            'probability_id': self.chance_prob.id,
            'profit_id': False,
        })
        self.assertFalse(table.chance_level)
        table.write({
            'probability_id': False,
            'profit_id': self.chance_prof.id,
        })
        self.assertFalse(table.chance_level)
        table.write({
            'probability_id': self.chance_prob.id,
            'profit_id': self.chance_prof.id,
        })
        self.assertTrue(table.chance_level)
        self.assertEquals(
            round(table.chance_level, 4),
            round(self.chance_prof.qualification *
                  self.chance_prob.qualification, 4))

    def test_onchange_risk_id(self):
        table = self.table_model.create({
            'project_id': self.project.id,
            'risk_id': self.risk.id,
        })
        self.assertFalse(table.risk)
        table.onchange_risk_id()
        self.assertEquals(table.risk,
                          table.risk_id.name)

    def test_onchange_action_id(self):
        table = self.table_model.create({
            'project_id': self.project.id,
            'action_id': self.action.id,
        })
        self.assertFalse(table.action)
        table.onchange_action_id()
        self.assertEquals(table.action,
                          table.action_id.name)

    def test_onchange_chance_id(self):
        table = self.chance_model.create({
            'project_id': self.project.id,
            'chance_id': self.chance.id,
        })
        self.assertFalse(table.chance)
        table.onchange_chance_id()
        self.assertEquals(table.chance,
                          table.chance_id.name)

    def test_prob_onchange(self):
        table = self.chance_model.create({
            'project_id': self.project.id,
            'action_id': self.action.id,
        })
        self.assertFalse(table.action)
        table.onchange_action_id()
        self.assertEquals(table.action,
                          table.action_id.name)
