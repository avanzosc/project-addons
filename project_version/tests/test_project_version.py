# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectVersion(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProjectVersion, cls).setUpClass()
        cls.project_model = cls.env['project.project']
        cls.project = cls.project_model.create({
            'name': 'Test Project',
        })

    def test_project_version_vs_copy(self):
        self.assertEquals(self.project.version, 1)
        self.project.button_new_version()
        self.assertEquals(self.project.version, 2)
        old_versions = self.project_model.with_context(
            active_test=False).search([
                ('parent_id', '=', self.project.id),
                '&', ('historical_user_id', '=', False),
                ('historical_date', '=', False)
            ])
        self.assertEquals(len(old_versions), self.project.version - 1)
        project = self.project.copy()
        self.assertEquals(project.version, 1)
        self.assertNotEquals(project.version, self.project.version)

    def test_project_historify(self):
        self.assertEquals(self.project.version, 1)
        history_versions = self.project_model.with_context(
            active_test=False).search([
                ('parent_id', '=', self.project.id),
                '|', ('historical_user_id', '!=', False),
                ('historical_date', '!=', False)
            ])
        self.assertEquals(len(history_versions), 0)
        self.project.button_historical()
        history_versions = self.project_model.with_context(
            active_test=False).search([
                ('parent_id', '=', self.project.id),
                '|', ('historical_user_id', '!=', False),
                ('historical_date', '!=', False)
            ])
        self.assertEquals(self.project.version, 1)
        self.assertEquals(len(history_versions), 1)
        history_versions[:1].button_historical()
        new_history_versions = self.project_model.with_context(
            active_test=False).search([
                ('parent_id', '=', history_versions[:1].id),
                '|', ('historical_user_id', '!=', False),
                ('historical_date', '!=', False)
            ])
        self.assertEquals(len(new_history_versions), 0)
        history_versions[:1].button_new_version()
        old_versions = self.project_model.with_context(
            active_test=False).search([
                ('parent_id', '=', history_versions[:1].id),
                ('historical_user_id', '=', False),
                ('historical_date', '=', False)
            ])
        self.assertEquals(len(old_versions), 0)
