# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from .project_project import get_month_startdate_enddate

date2str = fields.Date.to_string
str2date = fields.Date.from_string


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    payroll_ids = fields.One2many(
        comodel_name='hr.employee.payroll', inverse_name='employee_id',
        string='Monthly Payroll')

    def button_compute_monthly_payroll(self):
        self.compute_monthly_payroll()
        return True

    def compute_monthly_payroll(self, date=None):
        if not date:
            date = fields.Date.today()
        account = self.env.ref('project_analysis.employee_payroll_account')
        analytic_line_obj = self.env['account.analytic.line']
        startdate, enddate = get_month_startdate_enddate(date)
        for employee in self:
            employee.payroll_ids.filtered(
                lambda p: p.date == date2str(startdate)).unlink()
            analytic_lines = analytic_line_obj.search([
                ('date', '>=', startdate), ('date', '<=', enddate),
                ('move_id.partner_id', '=', employee.address_id.id),
                ('account_id', '=', account.id),
            ])
            employee.payroll_ids.create({
                'date': startdate,
                'employee_id': employee.id,
                'payroll': sum(analytic_lines.mapped('amount')),
            })

    def button_compute_all_monthly_payroll(self):
        account = self.env.ref('project_analysis.employee_payroll_account')
        analytic_lines = self.env['account.analytic.line'].search([
            ('account_id', '=', account.id),
        ], limit=1, order='date ASC')
        today = str2date(fields.Date.today())
        date = str2date(analytic_lines[:1].date) or today
        while date < today:
            self.compute_monthly_payroll(date=date)
            date += relativedelta(months=1)


class HrEmployeePayroll(models.Model):
    _name = 'hr.employee.payroll'

    date = fields.Date(string='Date')
    employee_id = fields.Many2one(
        comodel_name='hr.employee', required=True, string='Employee')
    payroll = fields.Float(string='Payroll')

    _sql_constraints = [
        ('employee_payroll_month_unique',
         'unique(date, employee_id)',
         'There can only be one payroll per month'),
    ]
