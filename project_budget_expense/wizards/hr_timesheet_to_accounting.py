# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class HrTimesheet2Accounting(models.TransientModel):
    _name = 'hr.timesheet.accounting'
    _description = 'Wizard to make account move from timesheets'

    line_ids = fields.Many2many(
        comodel_name='account.analytic.line', string='Timesheets')

    @api.model
    def default_get(self, fields_list):
        defaults = super(HrTimesheet2Accounting, self).default_get(fields_list)
        active_lines = self.env['account.analytic.line'].browse(
            self.env.context.get('active_ids'))
        lines = active_lines.filtered(lambda l: l.employee_id and not l.move_id)
        defaults.update({
            'line_ids': [(6, 0, lines.ids)],
        })
        return defaults

    def button_create_account_move(self):
        lines = self.line_ids.filtered(
            lambda l: not l.move_id and l.employee_id)
        amount = abs(sum(lines.mapped('amount')))
        qty = sum(lines.mapped('unit_amount'))
        payable_line_vals = {
            'account_id': self.env.ref(
                'project_budget_expense.account_account_employee_payable').id,
            'debit': amount,
            'quantity': qty,
            'analytic_line_ids': [(6, 0, lines.ids)],
        }
        receivable_line_vals = {
            'account_id': self.env.ref(
                'project_budget_expense.account_account_employee_receivable').id,
            'credit': amount,
            'quantity': qty,
        }
        self.env['account.move'].create({
            'date': fields.Date.context_today(self),
            'journal_id': self.env.ref(
                'project_budget_expense.account_journal_employee').id,
            'line_ids': [(0, 0, payable_line_vals),
                         (0, 0, receivable_line_vals)]
        })
        return True
