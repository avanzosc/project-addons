# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectRisk(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProjectRisk, cls).setUpClass()
        cls.table_model = cls.env['project.risk.table']
        cls.probability = cls.env.ref('project_risk.probab1')
        cls.impact = cls.env.ref('project_risk.impact1')
        cls.project = cls.env['project.project'].create({
            'name': 'Test Project',
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
