# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from collections import OrderedDict

from odoo.osv import expression
from odoo.tests import common, tagged
from odoo.tools.safe_eval import safe_eval


@tagged("post_install", "-at_install")
class TestProjectSaleUtilities(common.SavepointCase):
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
                "name": "Test Customer",
            }
        )
        cls.project = cls.env["project.project"].create(
            {
                "name": "Test Project",
                "partner_id": cls.partner.id,
            }
        )
        cls.project._create_analytic_account()
        cls.sale_model = cls.env["sale.order"]
        cls.sale = cls.sale_model.create(
            {
                "partner_id": cls.partner.id,
                "analytic_account_id": cls.project.analytic_account_id.id,
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
                        },
                    )
                    for p in cls.products.values()
                ],
            }
        )
        cls.invoice_model = cls.env["account.move"]

    def test_project_sale_out_invoice(self):
        inv = self.create_invoice_from_sale_order()
        self.assertEqual(self.project.out_invoice_count, 1.0)
        self.assertEqual(
            self.project.out_invoiced,
            sum(inv.mapped("invoice_line_ids.price_subtotal")),
        )
        line_domain = [
            (
                "analytic_account_id",
                "in",
                self.project.mapped("analytic_account_id").ids,
            ),
            ("move_id.move_type", "=", "out_invoice"),
        ]
        invoice_lines = self.env["account.move.line"].search(line_domain)
        invoice_action = self.browse_ref("account.action_move_out_invoice_type")
        invoice_domain = expression.AND(
            [
                [("id", "in", invoice_lines.mapped("move_id").ids)],
                safe_eval(invoice_action.domain or "[]"),
            ]
        )
        invoice_dict = self.project.button_open_out_invoice()
        self.assertEqual(invoice_dict.get("domain"), invoice_domain)
        invoice_line_domain = self.project._get_out_invoiced(domain=True)
        invoice_line_dict = self.project.button_open_out_invoice_line()
        self.assertEqual(invoice_line_dict.get("domain"), invoice_line_domain)

    def create_invoice_from_sale_order(self):
        self.assertTrue(self.sale.state == "draft")
        self.sale.action_confirm()
        self.assertTrue(self.sale.state == "sale")
        self.assertTrue(self.sale.invoice_status == "to invoice")
        inv = self.sale._create_invoices()
        self.assertTrue(
            self.sale.invoice_status == "no",
            'Sale: SO status after invoicing should be "nothing to invoice"',
        )
        self.assertEqual(len(inv.invoice_line_ids), 1, "Sale: invoice is missing lines")
        self.assertTrue(len(self.sale.invoice_ids) == 1, "Sale: invoice is missing")
        return inv
