# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectCloseInfo(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProjectCloseInfo, cls).setUpClass()
        cls.project_model = cls.env['project.project']
        cls.criteria_model = cls.env['project.close.template']
        cls.criteria_model.create({
            'name': 'Test Criteria',
        })
        cls.project = cls.project_model.create({
            'name': 'Test Project',
        })

    def test_project_close_info(self):
        criterias = self.criteria_model.search([])
        self.assertEquals(len(self.project.criteria_ids), len(criterias))
        self.assertTrue(self.project.active)
        for criteria in self.project.with_context(
                active_test=False).criteria_ids:
            self.assertTrue(criteria.active)
        self.project.toggle_active()
        self.assertFalse(self.project.active)
        for criteria in self.project.with_context(
                active_test=False).criteria_ids:
            self.assertFalse(criteria.active)
        self.project.toggle_active()
        self.assertTrue(self.project.active)
        for criteria in self.project.with_context(
                active_test=False).criteria_ids:
            self.assertTrue(criteria.active)
