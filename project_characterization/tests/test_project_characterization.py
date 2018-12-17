# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectCharacterization(common.TransactionCase):

    def setUp(self):
        super(TestProjectCharacterization, self).setUp()
        res_partner_model = self.env['res.partner']
        self.project_model = self.env['project.project']
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
