# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectViability(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProjectViability, cls).setUpClass()
        cls.factor_model = cls.env['project.viability.factor']
        cls.project_model = cls.env['project.project']
        cls.template = cls.env['project.viability.template'].create({
            'name': 'Template',
            'factor_ids': [(4, x.id) for x in cls.factor_model.search([])],
        })
        cls.setting = cls.env['res.config.settings'].create({})

    def test_project_creation(self):
        self.setting.viability_templ_id = self.template
        self.setting.set_values()
        project = self.project_model.create({
            'name': 'Project',
        })
        self.assertEquals(
            project.viability_templ_id, self.template)
        self.assertEquals(
            len(project.viability_line_ids), len(self.template.factor_ids))
        self.assertEquals(
            len(project.viability_categ_line_ids),
            len(self.template.categ_ids))
        self.assertEquals(project.viability_score, 0.0)

    def test_res_config(self):
        self.assertFalse(
            self.setting.viability_templ_id)
        self.setting.viability_templ_id = (
            self.setting._default_viability_template())
        self.setting.set_values()
        self.assertTrue(
            self.setting.viability_templ_id)

    def test_name_gets(self):
        code = name = 'TEST'
        category = self.env['project.viability.category'].create({
            'code': code,
            'name': name,
        })
        self.assertEquals(
            category.display_name, '[{}] {}'.format(code, name))
        factor = self.env['project.viability.factor'].create({
            'code': code,
            'name': name,
            'categ_id': category.id,
        })
        self.assertEquals(
            factor.display_name, '[{}-{}] {}'.format(code, code, name))
