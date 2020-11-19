# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tools.safe_eval import safe_eval
from odoo.tests import common
from collections import OrderedDict
from odoo.osv import expression


@common.at_install(False)
@common.post_install(True)
class TestProjectSaleUtilities(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProjectSaleUtilities, cls).setUpClass()
        cls.products = OrderedDict([
            ('prod_order', cls.env.ref('product.product_order_01')),
            ('serv_del', cls.env.ref('product.service_delivery')),
            ('serv_order', cls.env.ref('product.service_order_01')),
            ('prod_del', cls.env.ref('product.product_delivery_01')),
        ])
        cls.partner = cls.env["res.partner"].create({
            "name": "Test Customer",
            "customer": True,
        })
        cls.project = cls.env["project.project"].create({
            "name": "Test Project",
            "partner_id": cls.partner.id,
        })
        cls.sale_model = cls.env["sale.order"]
        cls.sale = cls.sale_model.create({
            "partner_id": cls.partner.id,
            "analytic_account_id": cls.project.analytic_account_id.id,
            "order_line": [(0, 0, {
                "name": p.name,
                "product_id": p.id,
                "product_uom_qty": 2,
                "product_uom": p.uom_id.id,
                "price_unit": p.list_price}) for p in cls.products.values()],
        })
        cls.invoice_model = cls.env['account.invoice']

    def test_project_sale_out_invoice(self):
        inv = self.create_invoice_from_sale_order()
        self.assertEquals(self.project.out_invoice_count, 1.0)
        self.assertEquals(
            self.project.out_invoiced,
            sum(inv.mapped("invoice_line_ids.price_subtotal")))
        line_domain = [
            ("account_analytic_id", "in",
             self.project.mapped("analytic_account_id").ids),
            ("invoice_type", "in", ["out_invoice", "out_refund"])]
        lines = self.env["account.invoice.line"].search(line_domain)
        invoice_action = self.browse_ref(
            "account.action_invoice_refund_out_tree")
        invoice_domain = expression.AND([
            [("id", "in", lines.mapped("invoice_id").ids)],
            safe_eval(invoice_action.domain or "[]")])
        invoice_dict = self.project.button_open_out_invoice()
        self.assertEquals(invoice_dict.get("domain"), invoice_domain)
        line_dict = self.project.button_open_out_invoice_line()
        self.assertEquals(line_dict.get("domain"), line_domain)

    def create_invoice_from_sale_order(self):
        self.assertTrue(self.sale.state == "draft")
        self.sale.action_confirm()
        self.assertTrue(self.sale.state == "sale")
        self.assertTrue(self.sale.invoice_status == "to invoice")
        inv_id = self.sale.action_invoice_create()
        inv = self.invoice_model.browse(inv_id)
        self.assertTrue(
            self.sale.invoice_status == "no",
            'Sale: SO status after invoicing should be "nothing to invoice"')
        self.assertEqual(
            len(inv.invoice_line_ids), 2, "Sale: invoice is missing lines")
        self.assertTrue(
            len(self.sale.invoice_ids) == 1, "Sale: invoice is missing")
        return inv
