# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def _timesheet_preprocess(self, vals):
        vals = super(AccountAnalyticLine, self)._timesheet_preprocess(vals)
        if vals.get('employee_id') and not vals.get('general_account_id'):
            employee = self.env['hr.employee'].browse(vals['employee_id'])
            vals['general_account_id'] = (
                employee.property_account_payable_id.id)
        return vals

    def _cron_create_account_move(self):
        timesheets = self.search([
            ('project_id', '!=', False), ('employee_id', '!=', False),
            ('move_id', '=', False)])
        wiz = self.env['hr.timesheet.accounting'].with_context(
            active_ids=timesheets.ids).create({})
        wiz.button_create_account_move()
