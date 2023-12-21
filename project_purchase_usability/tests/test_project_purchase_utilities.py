# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from collections import OrderedDict

from odoo.osv import expression
from odoo.tests import common, tagged
from odoo.tools.safe_eval import safe_eval


@tagged("post_install", "-at_install")
class TestProjectPurchaseUtilities(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.products = OrderedDict(
            [
                ("prod_order", cls.env.ref("product.product_order_01")),
                ("prod_del", cls.env.ref("product.product_delivery_01")),
            ]
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Supplier",
            }
        )
        cls.project = cls.env["project.project"].create(
            {
                "name": "Test Project",
                "partner_id": cls.partner.id,
            }
        )
        cls.project._create_analytic_account()
        cls.purchase_model = cls.env["purchase.order"]
        cls.purchase = cls.purchase_model.create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": p.name,
                            "product_id": p.id,
                            "product_uom_qty": 2,
                            "product_uom": p.uom_id.id,
                            "price_unit": p.list_price,
                            "account_analytic_id": cls.project.analytic_account_id.id,
                        },
                    )
                    for p in cls.products.values()
                ],
            }
        )
        cls.invoice_model = cls.env["account.move"]

    def test_project_purchase(self):
        self.assertTrue(self.purchase)
        self.assertEqual(self.project.purchase_count, 1)
        self.assertEqual(
            self.project.purchase_line_count, len(self.purchase.order_line)
        )
        purchase_domain = [
            (
                "account_analytic_id",
                "in",
                self.project.mapped("analytic_account_id").ids,
            )
        ]
        purchase_lines = self.env["purchase.order.line"].search(purchase_domain)
        order_domain = [("id", "in", purchase_lines.mapped("order_id").ids)]
        purchase_dict = self.project.button_open_purchase_order()
        self.assertEqual(purchase_dict.get("domain"), order_domain)
        purchase_line_dict = self.project.button_open_purchase_order_line()
        self.assertEqual(purchase_line_dict.get("domain"), purchase_domain)

    def test_project_purchase_in_invoice(self):
        self.assertFalse(self.project.in_invoiced)
        self.assertFalse(self.project.in_invoice_count)
        self.create_invoice_from_purchase_order()
        self.assertTrue(self.purchase.invoice_ids)
        self.project.invalidate_cache()
        self.assertEqual(self.project.in_invoice_count, 1)
        invoice_lines = self.project._get_in_invoiced()
        self.assertEqual(
            self.project.in_invoiced,
            sum(invoice_lines.mapped("price_subtotal")),
        )
        invoice_action = self.browse_ref("account.action_move_in_invoice_type")
        invoice_domain = expression.AND(
            [
                [("id", "in", invoice_lines.mapped("move_id").ids)],
                safe_eval(invoice_action.domain or "[]"),
            ]
        )
        invoice_dict = self.project.button_open_in_invoice()
        self.assertEqual(invoice_dict.get("domain"), invoice_domain)
        invoice_line_domain = self.project._get_in_invoiced(domain=True)
        invoice_line_dict = self.project.button_open_in_invoice_line()
        self.assertEqual(invoice_line_dict.get("domain"), invoice_line_domain)

    def create_invoice_from_purchase_order(self):
        self.assertTrue(self.purchase.state == "draft")
        self.purchase.button_confirm()
        self.assertEqual(self.purchase.invoice_status, "no")
        for line in self.purchase.order_line:
            self.assertEqual(line.qty_to_invoice, 0.0)
            self.assertEqual(line.qty_invoiced, 0.0)
        self.purchase.order_line.qty_received = 5
        self.assertEqual(self.purchase.invoice_status, "to invoice")
        for line in self.purchase.order_line:
            self.assertEqual(line.qty_to_invoice, 5)
            self.assertEqual(line.qty_invoiced, 0.0)
        self.purchase.action_create_invoice()
        self.assertEqual(self.purchase.invoice_status, "invoiced")
        for line in self.purchase.order_line:
            self.assertEqual(line.qty_to_invoice, 0.0)
            self.assertEqual(line.qty_invoiced, 5)
