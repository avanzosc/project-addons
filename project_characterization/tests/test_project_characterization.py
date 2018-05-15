# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProjectCharacterization(common.TransactionCase):

    def setUp(self):
        super(TestProjectCharacterization, self).setUp()
        res_partner_model = self.env['res.partner']
        funding_src_model = self.env['funding.source']
        project_model = self.env['project.project']
        self.funding_project_model = self.env['funding.source.project']
        self.partner = res_partner_model.create({
            'name': 'Test Partner',
        })
        self.funding_src = funding_src_model.create({
            'name': 'Test Funding Source',
        })
        self.project = project_model.create({
            'name': 'Test Project',
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
