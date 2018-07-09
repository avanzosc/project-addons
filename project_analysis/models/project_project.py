# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from dateutil.relativedelta import relativedelta
import calendar
from odoo import api, fields, models

str2date = fields.Date.from_string
date2str = fields.Date.to_string


def get_month_startdate_enddate(date=None):
    if not date:
        date = fields.Date.today()
    date = str2date(date) if isinstance(date, str) else date
    date -= relativedelta(months=1)
    (weekday, lastday) = calendar.monthrange(date.year, date.month)
    startdate = date.replace(day=1)
    enddate = date.replace(day=lastday)
    return startdate, enddate


class ProjectProject(models.Model):
    _inherit = 'project.project'

    resume_id = fields.One2many(
        comodel_name='project.analytic.summary', inverse_name='project_id',
        string='Summary', readonly=True)
    monthly_hour_ids = fields.One2many(
        comodel_name='project.analytic.monthly_hour', inverse_name='project_id',
        string='Monthly Hours')
    monthly_line_ids = fields.One2many(
        comodel_name='project.analytic.monthly_line', inverse_name='project_id',
        string='Monthly Cost/Revenue')
    monthly_nonoperative_ids = fields.One2many(
        comodel_name='project.analytic.nonoperative', inverse_name='project_id',
        string='Non Operative Monthly Cost/Revenue')

    @api.multi
    def button_compute_monthly_hour(self):
        self.compute_monthly_hour()
        return True

    def compute_monthly_hour(self, date=None):
        if not date:
            date = fields.Date.today()
        startdate, enddate = get_month_startdate_enddate(date)
        hour_obj = hours = self.env['project.analytic.monthly_hour']
        for project in self:
            project.monthly_hour_ids.filtered(
                lambda l: l.timesheet_date == date2str(startdate)).unlink()
            self.env.cr.execute("""
                SELECT
                  date_trunc('month', date) AS timesheet_date,
                  SUM(unit_amount) AS unit_amount,
                  project_id,
                  employee_id
                FROM
                  account_analytic_line
                WHERE
                  project_id = %s
                  AND date >= %s
                  AND date <= %s
                  AND employee_id IS NOT NULL
                GROUP BY
                  project_id, timesheet_date, employee_id;
            """, (project.id, startdate, enddate))
            lines = self.env.cr.dictfetchall()
            for line in lines:
                hours |= hour_obj.create(line)

    @api.multi
    def button_compute_monthly_line(self):
        self.compute_monthly_line()
        return True

    def compute_monthly_line(self, date=None):
        if not date:
            date = fields.Date.today()
        startdate, enddate = get_month_startdate_enddate(date)
        line_obj = monthlines = self.env['project.analytic.monthly_line']
        for project in self:
            project.monthly_line_ids.filtered(
                lambda l: l.timesheet_date == date2str(startdate)).unlink()
            self.env.cr.execute("""
                SELECT
                  date_trunc('month', date) AS timesheet_date,
                  SUM(amount) AS amount
                FROM
                  account_analytic_line
                WHERE
                  account_id = %s
                  AND date >= %s
                  AND date <= %s
                  AND project_id IS NULL
                GROUP BY
                  account_id, timesheet_date;
            """, (project.analytic_account_id.id, startdate, enddate))
            lines = self.env.cr.dictfetchall()
            for line in lines:
                line.update({'project_id': project.id})
                monthlines |= line_obj.create(line)
            if not lines:
                line_obj.create({
                    'project_id': project.id,
                    'timesheet_date': startdate,
                })

    @api.multi
    def button_compute_monthly_nonoperative(self):
        self.compute_monthly_nonoperative()
        return True

    def compute_monthly_nonoperative(self, date=None):
        if not date:
            date = fields.Date.today()
        startdate, enddate = get_month_startdate_enddate(date)
        area_obj = self.env['res.area']
        amount_obj = self.env['project.analytic.nonoperative']
        for project in self.filtered(
                lambda p: not p.nonoperative and p.res_area_id):
            project.monthly_nonoperative_ids.filtered(
                lambda l: l.timesheet_date == date2str(startdate)).unlink()
            areas = area_obj.search([
                ('related_operative_area_ids', 'in', project.res_area_id.id)])
            nonop_projects = self.search([
                ('res_area_id', 'in', areas.ids)])
            nonop_projects.button_compute_monthly_line()
            lines = nonop_projects.mapped('monthly_line_ids').filtered(
                lambda l: l.timesheet_date == date2str(startdate))
            amount = sum(lines.mapped('amount'))
            amount_obj.create({
                'project_id': project.id,
                'timesheet_date': startdate,
                'amount': amount,
            })

    @api.multi
    def button_compute_summary(self):
        startdate, enddate = get_month_startdate_enddate()
        summary_obj = summaries = self.env['project.analytic.summary']
        for project in self:
            project.button_compute_monthly_hour()
            self.env.cr.execute("""
                SELECT
                  date_trunc('month', date) AS timesheet_date,
                  SUM(unit_amount) AS unit_amount,
                  project_id,
                  employee_id
                FROM
                  account_analytic_line
                WHERE
                  project_id = %s
                  AND date >= %s
                  AND date <= %s
                GROUP BY
                  project_id, employee_id, timesheet_date;
            """, (project.id, startdate, enddate))
            lines = self.env.cr.dictfetchall()
            for line in lines:
                summaries |= summary_obj.create(line)
        return True


class ProjectAnalyticMonthlyHours(models.Model):
    _name = 'project.analytic.monthly_hour'
    _order = 'project_id, timesheet_date'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project', required=True)
    employee_id = fields.Many2one(
        comodel_name='hr.employee', string='Employee')
    timesheet_date = fields.Date(string='Date')
    unit_amount = fields.Float(string='Quantity')


class ProjectAnalyticMonthlyLine(models.Model):
    _name = 'project.analytic.monthly_line'
    _order = 'project_id, timesheet_date'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project', required=True)
    timesheet_date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')
    payroll = fields.Float(string='Payroll', compute='_compute_payroll')

    @api.depends('timesheet_date')
    def _compute_payroll(self):
        account = self.env.ref('project_analysis.employee_payroll_account')
        analytic_line_obj = self.env['account.analytic.line']
        for line in self:
            startdate, enddate = get_month_startdate_enddate(
                line.timesheet_date)
            analytic_lines = analytic_line_obj.search([
                ('date', '>=', startdate), ('date', '<=', enddate),
                ('account_id', '=', account.id),
            ])
            line.payroll = sum(analytic_lines.mapped('amount'))


class ProjectAnalyticMonthlyNonoperative(models.Model):
    _name = 'project.analytic.nonoperative'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project', required=True)
    timesheet_date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')


class ProjectAnalyticSummary(models.Model):
    _name = 'project.analytic.summary'
    _description = 'Timesheet Summary per Project'
    _order = 'project_id, timesheet_date, employee_id'

    timesheet_date = fields.Date(string='Date')
    project_id = fields.Many2one(
        comodel_name='project.project', string='Project', required=True)
    employee_id = fields.Many2one(
        comodel_name='hr.employee', string='Employee', required=True)
    unit_amount = fields.Float(string='Quantity')
    monthly_amount = fields.Float(
        string='Monthly Quantity', compute='_compute_monthly_amount',
        store=True, group_operator='avg')
    percent_amount = fields.Float(
        string='Amount Percent', compute='_compute_monthly_amount',
        store=True, group_operator='sum')
    payroll = fields.Float(
        string='Payroll', compute='_compute_payroll',)
        # store=True, group_operator='sum')
    monthly_payroll = fields.Float(
        string='Monthly Payroll', compute='_compute_monthly_payroll',)
        # store=True, group_operator='avg')
    percent_payroll = fields.Float(
        string='Payroll Percent', compute='_compute_monthly_payroll',)
    #     # store=True, group_operator='sum')

    def compute_all(self):
        created = self
        self.env.cr.execute("""
            SELECT
              date_trunc('month', date) AS timesheet_date,
              project_id,
              employee_id,
              SUM(unit_amount) AS unit_amount
            FROM
              account_analytic_line
            WHERE
              project_id IS NOT NULL
            GROUP BY
              project_id, employee_id, timesheet_date;
        """)
        lines = self.env.cr.dictfetchall()
        for line in lines:
            created |= self.create(line)
        created._compute_monthly_amount()
        return True

    @api.depends('timesheet_date', 'unit_amount', 'project_id.monthly_hour_ids',
                 'project_id.monthly_hour_ids.unit_amount', 'employee_id')
    def _compute_monthly_amount(self):
        hour_obj = self.env['project.analytic.monthly_hour']
        for line in self:
            line.monthly_amount = sum(hour_obj.search([
                ('timesheet_date', '=', line.timesheet_date),
                ('employee_id', '=', line.employee_id.id),
            ]).mapped('unit_amount'))
            if line.monthly_amount:
                line.percent_amount = (
                    (line.unit_amount / line.monthly_amount) * 100.0)

    @api.depends('unit_amount', 'monthly_amount')
    def _compute_payroll(self):
        account = self.env.ref('project_analysis.employee_payroll_account')
        analytic_line_obj = self.env['account.analytic.line']
        account_group = self.env.ref('l10n_es.account_group_64')
        move_line_obj = self.env['account.move.line']
        for line in self.filtered('monthly_amount'):
            startdate, enddate = get_month_startdate_enddate(
                line.timesheet_date)
            analytic_lines = analytic_line_obj.search([
                ('date', '>=', startdate), ('date', '<=', enddate),
                ('move_id.partner_id', '=', line.employee_id.address_id.id),
                ('account_id', '=', account.id),
                # '|', ('general_account_id.group_id', '=', account_group.id),
                # ('general_account_id.group_id', 'child_of', account_group.id),
            ])
            # move_lines = move_line_obj.search([
            #     ('date', '=', line.timesheet_date),
            #     ('partner_id', '=', line.employee_id.address_id.id),
            #     '|', ('account_id.group_id', '=', account_group.id),
            #     ('account_id.group_id', 'child_of', account_group.id),
            # ])
            percent = line.unit_amount / line.monthly_amount
            line.payroll = sum(analytic_lines.mapped('amount')) * percent
            # line.payroll = sum(move_lines.mapped('debit')) * percent

    @api.depends('timesheet_date', 'payroll', 'project_id.monthly_line_ids',
                 'project_id.monthly_line_ids.payroll')
    def _compute_monthly_payroll(self):
        for line in self:
            line.monthly_payroll = line.project_id.monthly_line_ids.filtered(
                lambda l: l.timesheet_date == line.timesheet_date).payroll
            if line.monthly_payroll:
                line.percent_payroll = (
                    (line.payroll / line.monthly_payroll) * 100.0)
