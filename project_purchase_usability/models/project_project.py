# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class ProjectProject(models.Model):
    _inherit = "project.project"

    purchase_count = fields.Integer(
        compute="_compute_purchase_count", string="# Purchase"
    )
    purchase_line_count = fields.Integer(
        compute="_compute_purchase_count", string="# Purchase Line"
    )
    in_invoice_count = fields.Integer(
        compute="_compute_in_invoiced", string="# Purchase Invoice"
    )
    in_invoiced = fields.Monetary(compute="_compute_in_invoiced", string="In Invoiced")
    in_refund_count = fields.Integer(
        compute="_compute_in_refund", string="# Purchase Refund"
    )
    in_refund = fields.Monetary(compute="_compute_in_refund", string="In Refund")

    def _get_in_invoiced(self, domain=False):
        filter_domain = [
            ("analytic_account_id", "in", self.mapped("analytic_account_id").ids),
            ("move_id.move_type", "=", "in_invoice"),
        ]
        if domain:
            return filter_domain
        invoice_lines = self.env["account.move.line"].search(filter_domain)
        return invoice_lines

    def _get_in_refund(self, domain=False):
        filter_domain = [
            ("analytic_account_id", "in", self.mapped("analytic_account_id").ids),
            ("move_id.move_type", "=", "in_refund"),
        ]
        if domain:
            return filter_domain
        invoice_lines = self.env["account.move.line"].search(filter_domain)
        return invoice_lines

    def _compute_purchase_count(self):
        for project in self:
            purchase_lines = self.env["purchase.order.line"].search(
                [("account_analytic_id", "=", project.analytic_account_id.id)]
            )
            project.purchase_count = len(purchase_lines.mapped("order_id"))
            project.purchase_line_count = len(purchase_lines)

    def _compute_in_invoiced(self):
        for project in self:
            lines = project._get_in_invoiced()
            project.in_invoiced = sum(lines.mapped("price_subtotal"))
            project.in_invoice_count = len(lines.mapped("move_id"))

    def _compute_in_refund(self):
        for project in self:
            lines = project._get_in_refund()
            project.in_refund = sum(lines.mapped("price_subtotal"))
            project.in_refund_count = len(lines.mapped("move_id"))

    def button_open_purchase_order(self):
        self.ensure_one()
        purchase_lines = self.env["purchase.order.line"].search(
            [("account_analytic_id", "in", self.mapped("analytic_account_id").ids)]
        )
        domain = [("id", "in", purchase_lines.mapped("order_id").ids)]
        return {
            "name": _("Purchase Order"),
            "domain": domain,
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "purchase.order",
        }

    def button_open_purchase_order_line(self):
        self.ensure_one()
        domain = [("account_analytic_id", "in", self.mapped("analytic_account_id").ids)]
        return {
            "name": _("Purchase Order Lines"),
            "domain": domain,
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "purchase.order.line",
        }

    def button_open_in_invoice(self):
        self.ensure_one()
        action = self.env.ref("account.action_move_in_invoice_type")
        action_dict = action.read()[0] if action else {}
        lines = self._get_in_invoiced()
        domain = expression.AND(
            [
                [("id", "in", lines.mapped("move_id").ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def button_open_in_refund(self):
        self.ensure_one()
        action = self.env.ref("account.action_invoice_tree")
        action_dict = action.read()[0] if action else {}
        lines = self._get_in_refund()
        domain = expression.AND(
            [
                [("id", "in", lines.mapped("move_id").ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def button_open_in_invoice_line(self):
        self.ensure_one()
        domain = self._get_in_invoiced(domain=True)
        return {
            "name": _("In Invoice Lines"),
            "domain": domain,
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "account.move.line",
        }

    def button_open_in_refund_line(self):
        self.ensure_one()
        domain = self._get_in_refund(domain=True)
        return {
            "name": _("In Refund Lines"),
            "domain": domain,
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "account.move.line",
        }
