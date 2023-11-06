# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class ProjectProject(models.Model):
    _inherit = "project.project"

    in_invoice_count = fields.Integer(
        compute="_compute_in_invoiced", string="# Purchase Invoice"
    )
    in_invoiced = fields.Monetary(
        string="In invoices invoiced", compute="_compute_in_invoiced")
    in_refund_count = fields.Integer(
        compute="_compute_in_refund", string="# Purchase Refund"
    )
    in_refund = fields.Monetary(
        string="In invoices refund", compute="_compute_in_refund")

    def _domain_purchase_invoice_line(self):
        query = self.env["account.move.line"]._search(
            [("move_id.state", "!=", "cancel"),
             ("move_id.move_type", "in", ["in_invoice", "in_refund"]),
             ]
        )
        query.add_where(
            "account_move_line.analytic_distribution ?| array[%s]",
            [str(project.analytic_account_id.id) for project in self],
        )
        query.order = None
        query_string, query_param = query.select(
            "account_move_line.id as id",
        )
        self._cr.execute(query_string, query_param)
        purchase_invoice_lines_ids = [
            int(record.get("id")) for record in self._cr.dictfetchall()
        ]
        domain = [("id", "in", purchase_invoice_lines_ids)]
        return domain

    def _get_in_invoiced(self, domain=False):
        filter_domain = expression.AND(
            [
                [("move_id.move_type", "=", "in_invoice")],
                self._domain_purchase_invoice_line(),
            ]
        )
        if domain:
            return filter_domain
        invoice_lines = self.env["account.move.line"].search(filter_domain)
        return invoice_lines

    def _get_in_refund(self, domain=False):
        filter_domain = expression.AND(
            [[("move_id.move_type", "=", "in_refund")],
                self._domain_sale_invoice_line(),]
        )
        if domain:
            return filter_domain
        invoice_lines = self.env["account.move.line"].search(filter_domain)
        return invoice_lines

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

    def button_open_in_invoice(self):
        self.ensure_one()
        lines = self._get_in_invoiced()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_move_in_invoice_type"
        )
        domain = expression.AND(
            [
                [("id", "in", lines.mapped("move_id").ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        context = safe_eval(action.get("context") or "{}")
        context.update({"group_by": ["payment_state"]})
        action.update(
            {
                "domain": domain,
                "context": context,
            }
        )
        return action

    def button_open_in_refund(self):
        self.ensure_one()
        lines = self._get_out_refund()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_move_in_refund_type"
        )
        domain = expression.AND(
            [
                [("id", "in", lines.mapped("move_id").ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        context = safe_eval(action.get("context") or "{}")
        context.update({"group_by": ["payment_state"]})
        action.update(
            {
                "domain": domain,
                "context": context,
            }
        )
        return action

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
