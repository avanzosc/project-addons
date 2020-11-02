# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tools.safe_eval import safe_eval
from odoo import _, api, fields, models
from odoo.osv import expression


class ProjectProject(models.Model):
    _inherit = "project.project"

    out_invoice_count = fields.Integer(
        compute="_compute_out_invoiced", string="# Sale Invoice")
    out_invoiced = fields.Monetary(
        compute="_compute_out_invoiced", string="Out Invoiced")

    @api.multi
    def _compute_out_invoiced(self):
        invoice_line_obj = self.env["account.invoice.line"]
        for project in self:
            lines = invoice_line_obj.search([
                ("account_analytic_id", "=", project.analytic_account_id.id),
                ("invoice_type", "in", ["out_invoice", "out_refund"]),
            ])
            project.out_invoiced = sum(lines.mapped("price_subtotal_signed"))
            project.out_invoice_count = len(lines.mapped("invoice_id"))

    @api.multi
    def button_open_out_invoice(self):
        self.ensure_one()
        action = self.env.ref("account.action_invoice_refund_out_tree")
        action_dict = action.read()[0] if action else {}
        lines = self.env["account.invoice.line"].search([
            ("account_analytic_id", "in",
             self.mapped("analytic_account_id").ids),
            ("invoice_type", "in", ["out_invoice", "out_refund"])])
        domain = expression.AND([
            [("id", "in", lines.mapped("invoice_id").ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict

    @api.multi
    def button_open_out_invoice_line(self):
        self.ensure_one()
        tree_view = self.env.ref(
            "project_sale_utilities.account_invoice_sale_line_tree_view")
        domain = [("account_analytic_id", "in",
                   self.mapped("analytic_account_id").ids),
                  ("invoice_type", "in", ["out_invoice", "out_refund"])]
        return {
            "name": _("Out Invoice Lines"),
            "domain": domain,
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "account.invoice.line",
            "view_id": tree_view.id,
        }
