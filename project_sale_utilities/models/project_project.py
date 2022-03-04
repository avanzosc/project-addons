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
    def _get_out_invoices(self, domain=False):
        filter_domain = [
            ('account_analytic_id', 'in', self.mapped("analytic_account_id").ids),
            ('invoice_id.type', 'in', ['out_invoice', 'out_refund'])]
        if domain:
            return filter_domain
        invoice_lines = self.env['account.invoice.line'].search(filter_domain)
        return invoice_lines

    @api.multi
    def _compute_out_invoiced(self):
        for project in self:
            lines = project._get_out_invoices()
            project.out_invoiced = sum(lines.mapped("price_subtotal_signed"))
            project.out_invoice_count = len(lines.mapped("invoice_id"))

    @api.multi
    def button_open_out_invoice(self):
        self.ensure_one()
        action = self.env.ref("account.action_invoice_tree")
        action_dict = action.read()[0] if action else {}
        lines = self._get_out_invoices()
        domain = expression.AND([
            [("id", "in", lines.mapped("invoice_id").ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict

    @api.multi
    def button_open_out_invoice_line(self):
        self.ensure_one()
        domain = self._get_out_invoices(domain=True)
        return {
            "name": _("Out Invoice Lines"),
            "domain": domain,
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "account.invoice.line",
        }
