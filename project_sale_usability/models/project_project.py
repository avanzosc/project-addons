# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class ProjectProject(models.Model):
    _inherit = "project.project"

    out_invoice_count = fields.Integer(
        compute="_compute_out_invoiced", string="# Sale Invoice"
    )
    out_invoiced = fields.Monetary(
        compute="_compute_out_invoiced", string="Out Invoiced"
    )
    out_refund_count = fields.Integer(
        compute="_compute_out_refund", string="# Sale Refund"
    )
    out_refund = fields.Monetary(compute="_compute_out_refund", string="Out Refund")

    def _get_out_invoiced(self, domain=False):
        filter_domain = [
            ("analytic_account_id", "in", self.mapped("analytic_account_id").ids),
            ("move_id.move_type", "=", "out_invoice"),
        ]
        if domain:
            return filter_domain
        invoice_lines = self.env["account.move.line"].search(filter_domain)
        return invoice_lines

    def _get_out_refund(self, domain=False):
        filter_domain = [
            ("analytic_account_id", "in", self.mapped("analytic_account_id").ids),
            ("move_id.move_type", "=", "out_refund"),
        ]
        if domain:
            return filter_domain
        invoice_lines = self.env["account.move.line"].search(filter_domain)
        return invoice_lines

    def _compute_out_invoiced(self):
        for project in self:
            lines = project._get_out_invoiced()
            project.out_invoiced = sum(lines.mapped("price_subtotal"))
            project.out_invoice_count = len(lines.mapped("move_id"))

    def _compute_out_refund(self):
        for project in self:
            lines = project._get_out_refund()
            project.out_refund = sum(lines.mapped("price_subtotal"))
            project.out_refund_count = len(lines.mapped("move_id"))

    def button_open_out_invoice(self):
        self.ensure_one()
        action = self.env.ref("account.action_move_out_invoice_type")
        action_dict = action.read()[0] if action else {}
        lines = self._get_out_invoiced()
        domain = expression.AND(
            [
                [("id", "in", lines.mapped("move_id").ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def button_open_out_refund(self):
        self.ensure_one()
        action = self.env.ref("account.action_move_out_refund_type")
        action_dict = action.read()[0] if action else {}
        lines = self._get_out_refund()
        domain = expression.AND(
            [
                [("id", "in", lines.mapped("move_id").ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def button_open_out_invoice_line(self):
        self.ensure_one()
        domain = self._get_out_invoiced(domain=True)
        return {
            "name": _("Out Invoice Lines"),
            "domain": domain,
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "account.move.line",
        }

    def button_open_out_refund_line(self):
        self.ensure_one()
        domain = self._get_out_refund(domain=True)
        return {
            "name": _("Out Refund Lines"),
            "domain": domain,
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "account.move.line",
        }
