# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectCharacterization(common.TransactionCase):

    def setUp(self):
        super(TestProjectCharacterization, self).setUp()
        res_partner_model = self.env['res.partner']
        funding_src_model = self.env['funding.source']
        self.partner = res_partner_model.create({
            'name': 'Test Partner',
        })
        self.funding_src = funding_src_model.create({
            'name': 'Test Funding Source',
        })

    def test_computed_field_funding_source_count(self):
        self.assertFalse(self.partner.funding_source_ids)
        self.funding_src.partner_id = self.partner
        self.assertIn(self.funding_src, self.partner.funding_source_ids)
        self.assertTrue(self.partner.funding_source_count,
                        len(self.partner.funding_source_ids))
