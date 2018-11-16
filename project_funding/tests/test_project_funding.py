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

    def test_project_disable_enable(self):
        self.assertTrue(self.project.active)
        for funding in self.project.with_context(
                active_test=False).funding_ids:
            self.assertTrue(funding.active)
        self.project.toggle_active()
        self.assertFalse(self.project.active)
        for funding in self.project.with_context(
                active_test=False).funding_ids:
            self.assertFalse(funding.active)
        self.project.toggle_active()
        self.assertTrue(self.project.active)
        for funding in self.project.with_context(
                active_test=False).funding_ids:
            self.assertTrue(funding.active)
