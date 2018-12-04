# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ProjectProject(models.Model):
    _inherit = 'project.project'

    billing_plan_count = fields.Integer(
        string='# Billing Plans', compute='_compute_billing_plan_count')

    @api.multi
    def _compute_billing_plan_count(self):
        plan_obj = self.env['account.analytic.billing.plan']
        for project in self:
            project.billing_plan_count = plan_obj.search_count(
                [('analytic_account_id', '=', project.analytic_account_id.id)])

    @api.multi
    def button_open_billing_plan(self):
        self.ensure_one()
        action = self.env.ref(
            'account_analytic_billing_plan.'
            'action_account_analytic_billing_plan')
        action_dict = action.read()[0] if action else {}
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        action_dict['context'].update(
            {'default_analytic_account_id': self.analytic_account_id.id,
             'search_default_no_invoiced': True})
        domain = expression.AND([
            [('analytic_account_id', '=', self.analytic_account_id.id)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain})
        return action_dict
