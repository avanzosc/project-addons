# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectPurchaseUtilities(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProjectPurchaseUtilities, cls).setUpClass()
        cls.project_model = cls.env['project.project']
        cls.project = cls.project_model.create({
            'name': 'Test Project',
        })
        cls.purchase_model = cls.env['purchase.order']
        cls.purchase = cls.purchase_model.search([
            ('state', 'in', ('draft', 'sent')),
        ], limit=1)
        cls.invoice_model = cls.env['account.invoice']

    def test_project_purchase(self):
        self.assertTrue(self.purchase)
        self.purchase.write({
            'invoice_status': 'to invoice',
        })
        self.assertFalse(self.project.purchase_count)
        self.assertFalse(self.project.purchase_line_count)
        self.assertFalse(self.project.purchase_invoice_count)
        self.assertFalse(self.project.purchase_invoice_line_count)
        self.purchase.order_line[:1].write({
            'account_analytic_id': self.project.analytic_account_id.id,
        })
        self.project.invalidate_cache()
        self.assertEquals(self.project.purchase_count, 1)
        self.assertEquals(self.project.purchase_line_count, 1)
        self.assertFalse(self.project.purchase_invoice_count)
        self.assertFalse(self.project.purchase_invoice_line_count)
        self.purchase.button_confirm()
        invoice = self.invoice_model.create({
            'partner_id': self.purchase.partner_id.id,
            'purchase_id': self.purchase.id,
            'type': 'in_invoice',
        })
        invoice.purchase_order_change()
        self.project.invalidate_cache()
        self.assertEquals(self.project.purchase_invoice_count, 1)
        self.assertEquals(self.project.purchase_invoice_line_count, 1)
