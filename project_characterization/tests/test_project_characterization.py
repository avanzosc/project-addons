# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectCharacterization(common.TransactionCase):

    def setUp(self):
        super(TestProjectCharacterization, self).setUp()
        res_partner_model = self.env['res.partner']
        self.project_model = self.env['project.project']
        self.analytic_model = (
            self.env['account.analytic.account'].with_context(
                mail_create_nosubscribe=True))
        area_model = self.env['res.area']
        area_type_model = self.env['res.area.type']
        self.partner = res_partner_model.create({
            'name': 'Test Partner',
        })
        self.project = self.project_model.create({
            'name': 'Test Project',
        })
        self.area = area_model.create({
            'code': 'TA',
            'name': 'Test Area',
            'nonoperative': True,
        })
        self.type = area_type_model.create({
            'code': 'TAT',
            'name': 'Test Area Type',
        })
        self.setting = self.env['res.config.settings'].create({})

    def test_area_nonoperative(self):
        self.assertEquals(
            self.project.nonoperative, self.project.res_area_id.nonoperative)
        self.assertFalse(self.project.nonoperative)
        self.project.write({
            'res_area_id': self.area.id,
        })
        self.project._onchange_area_id()
        self.assertEquals(
            self.project.nonoperative, self.project.res_area_id.nonoperative)
        self.assertTrue(self.project.nonoperative)

    def test_create_new_project(self):
        self.setting.manual_code = False
        self.setting.set_values()
        self.assertFalse(self.setting.manual_code)
        vals = {
            'name': 'New Project',
            'res_area_id': self.area.id,
            'res_area_type_id': self.type.id,
        }
        new_project = self.project_model.new(vals)
        new_project._onchange_area_type()
        vals.update({'num_code': new_project.num_code})
        new_project = self.project_model.create(vals)
        count = self.project_model.search_count([
            ('res_area_id', '=', self.area.id),
            ('res_area_type_id', '=', self.type.id),
        ])
        self.assertEquals(
            new_project.code,
            '{}.{}.{}'.format(self.area.code, self.type.code, count))

    def test_create_new_project_char(self):
        self.setting.manual_code = False
        self.setting.set_values()
        self.assertFalse(self.setting.manual_code)
        vals = {
            'name': 'New Project',
            'res_area_id': self.area.id,
            'res_area_type_id': self.type.id,
        }
        new_project = self.project_model.new(vals)
        new_project._onchange_area_type()
        vals.update({'num_code': '{}a'.format(new_project.num_code)})
        self.project_model.create(vals)
        count = self.project_model.search_count([
            ('res_area_id', '=', self.area.id),
            ('res_area_type_id', '=', self.type.id),
        ])
        new_project2 = self.project_model.new(vals)
        new_project2._onchange_area_type()
        vals.update({'num_code': new_project2.num_code})
        new_project2 = self.project_model.create(vals)
        self.assertEquals(
            new_project2.num_code, str(count + 1))

    def test_create_new_account(self):
        self.setting.manual_code = False
        self.setting.set_values()
        self.assertFalse(self.setting.manual_code)
        vals = {
            'name': 'New Project',
            'res_area_id': self.area.id,
            'res_area_type_id': self.type.id,
        }
        new_account = self.analytic_model.new(vals)
        new_account._onchange_area_type()
        vals.update({'num_code': new_account.num_code})
        new_account = self.analytic_model.create(vals)
        count = self.analytic_model.search_count([
            ('res_area_id', '=', self.area.id),
            ('res_area_type_id', '=', self.type.id),
        ])
        self.assertEquals(
            new_account.code,
            '{}.{}.{}'.format(self.area.code, self.type.code, count))

    def test_create_new_account_char(self):
        self.setting.manual_code = False
        self.setting.set_values()
        self.assertFalse(self.setting.manual_code)
        vals = {
            'name': 'New Project',
            'res_area_id': self.area.id,
            'res_area_type_id': self.type.id,
        }
        new_account = self.analytic_model.new(vals)
        new_account._onchange_area_type()
        vals.update({'num_code': '{}a'.format(new_account.num_code)})
        self.analytic_model.create(vals)
        count = self.analytic_model.search_count([
            ('res_area_id', '=', self.area.id),
            ('res_area_type_id', '=', self.type.id),
        ])
        new_account2 = self.analytic_model.new(vals)
        new_account2._onchange_area_type()
        vals.update({'num_code': new_account2.num_code})
        new_account2 = self.analytic_model.create(vals)
        self.assertEquals(
            new_account2.num_code, str(count + 1))

    def test_create_new_project_manual(self):
        self.setting.manual_code = True
        self.setting.set_values()
        self.assertTrue(self.setting.manual_code)
        vals = {
            'name': 'New Project',
            'res_area_id': self.area.id,
            'res_area_type_id': self.type.id,
        }
        new_project = self.project_model.new(vals)
        new_project._onchange_area_type()
        self.assertFalse(new_project.num_code)
        vals.update({'num_code': '10'})
        new_project = self.project_model.create(vals)
        self.assertEquals(
            new_project.code,
            '{}.{}.{}'.format(self.area.code, self.type.code,
                              new_project.num_code))

    def test_create_new_account_manual(self):
        self.setting.manual_code = True
        self.setting.set_values()
        self.assertTrue(self.setting.manual_code)
        vals = {
            'name': 'New Project',
            'res_area_id': self.area.id,
            'res_area_type_id': self.type.id,
        }
        new_account = self.analytic_model.new(vals)
        new_account._onchange_area_type()
        self.assertFalse(new_account.num_code)
        vals.update({'num_code': '10'})
        new_account = self.analytic_model.create(vals)
        self.assertEquals(
            new_account.code,
            '{}.{}.{}'.format(self.area.code, self.type.code,
                              new_account.num_code))
