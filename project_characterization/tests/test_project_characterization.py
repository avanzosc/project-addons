# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProjectCharacterization(common.TransactionCase):

    def setUp(self):
        super(TestProjectCharacterization, self).setUp()
        res_partner_model = self.env['res.partner']
        funding_src_model = self.env['funding.source']
        self.project_model = self.env['project.project']
        area_model = self.env['res.area']
        area_type_model = self.env['res.area.type']
        self.funding_project_model = self.env['funding.source.project']
        self.partner = res_partner_model.create({
            'name': 'Test Partner',
        })
        self.funding_src = funding_src_model.create({
            'name': 'Test Funding Source',
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

    def test_computed_field_funding_source_count(self):
        self.assertFalse(self.partner.funding_source_ids)
        self.funding_src.partner_id = self.partner
        self.assertIn(self.funding_src, self.partner.funding_source_ids)
        self.assertTrue(self.partner.funding_source_count,
                        len(self.partner.funding_source_ids))

    def test_funding_src_constraints(self):
        funding_project = self.funding_project_model.create({
            'project_id': self.project.id,
            'source_id': self.funding_src.id,
        })
        with self.assertRaises(ValidationError):
            funding_project.write({
                'percentage': -0.1,
            })
        with self.assertRaises(ValidationError):
            funding_project.write({
                'percentage': 100.1,
            })
        funding_project.write({
            'percentage': 50.0,
        })

    def test_show_analytic_account(self):
        result = self.project.show_analytic_account_from_project()
        domain = result.get('domain')
        self.assertEquals(domain,
                          [('id', '=', self.project.analytic_account_id.id)])

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
        new_project = self.project_model.create({
            'name': 'New Project',
            'res_area_id': self.area.id,
            'res_area_type_id': self.type.id,
        })
        count = self.project_model.search_count([
            ('res_area_id', '=', self.area.id),
            ('res_area_type_id', '=', self.type.id),
        ])
        self.assertEquals(
            new_project.code,
            '{}.{}.{}'.format(self.area.code, self.type.code, count))
