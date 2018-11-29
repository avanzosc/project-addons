# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectVersion(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProjectVersion, cls).setUpClass()
        project_model = cls.env['project.project']
        cls.project = project_model.create({
            'name': 'Test Project',
        })

    def test_project_version_vs_copy(self):
        self.assertEquals(self.project.version, 1)
        self.project.button_new_version()
        self.assertEquals(self.project.version, 2)
        project = self.project.copy()
        self.assertEquals(project.version, 1)
        self.assertNotEquals(project.version, self.project.version)
