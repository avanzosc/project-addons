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
        phase_model = cls.env['project.phase']
        cls.phase1 = cls.project_model._get_default_phase_id()
        cls.phase2 = phase_model.search([('sequence', '!=', '1')], limit=1)
        cls.setting = cls.env['res.config.settings'].create({})

    def test_project_phase_nohistorify(self):
        self.setting.phase_history = False
        self.setting.set_values()
        self.assertNotEquals(self.phase1, self.phase2)
        self.assertEquals(self.phase1, self.project.phase_id)
        history_versions = self.project_model.with_context(
            active_test=False).search([
                ('parent_id', '=', self.project.id),
                '|', ('historical_user_id', '!=', False),
                ('historical_date', '!=', False)
            ])
        self.assertEquals(len(history_versions), 0)
        self.project.phase_id = self.phase2
        history_versions = self.project_model.with_context(
            active_test=False).search([
                ('parent_id', '=', self.project.id),
                '|', ('historical_user_id', '!=', False),
                ('historical_date', '!=', False)
            ])
        self.assertEquals(len(history_versions), 0)

    def test_project_phase_historify(self):
        self.setting.phase_history = True
        self.setting.set_values()
        self.assertNotEquals(self.phase1, self.phase2)
        self.assertEquals(self.phase1, self.project.phase_id)
        history_versions = self.project_model.with_context(
            active_test=False).search([
                ('parent_id', '=', self.project.id),
                '|', ('historical_user_id', '!=', False),
                ('historical_date', '!=', False)
            ])
        self.assertEquals(len(history_versions), 0)
        self.project.phase_id = self.phase2
        history_versions = self.project_model.with_context(
            active_test=False).search([
                ('parent_id', '=', self.project.id),
                '|', ('historical_user_id', '!=', False),
                ('historical_date', '!=', False)
            ])
        self.assertEquals(len(history_versions), 1)
        self.assertNotEquals(
            self.project.phase_id, history_versions[:1].phase_id)

    def test_project_version(self):
        self.project.button_new_version()
        old_versions = self.project_model.with_context(
            active_test=False).search([
                ('parent_id', '=', self.project.id),
                '&', ('historical_user_id', '=', False),
                ('historical_date', '=', False)
            ])
        self.assertEquals(len(old_versions), self.project.version - 1)
        self.assertEquals(old_versions[:1].phase_id, self.project.phase_id)
        self.assertNotEquals(old_versions[:1].version, self.project.version)
