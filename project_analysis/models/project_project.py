# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    resume_id = fields.One2many(
        comodel_name='project.analytic.summary', inverse_name='project_id',
        string='Summary', readonly=True)


class ProjectAnalyticSummary(models.Model):
    _name = 'project.analytic.summary'
    _description = 'Timesheet Summary per Project'

    timesheet_date = fields.Date(string='Date')
    project_id = fields.Many2one(
        comodel_name='project.project', string='Project', required=True)
    employee_id = fields.Many2one(
        comodel_name='hr.employee', string='Employee', required=True)
    unit_amount = fields.Float(string='Quantity')
    monthly_amount = fields.Float(
        string='Monthly Quantity', compute='_compute_monthly_amount',
        store=True, group_operator='avg')

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

    @api.depends('timesheet_date', 'employee_id', 'unit_amount')
    def _compute_monthly_amount(self):
        for line in self:
            self.env.cr.execute("""
                SELECT
                  SUM(unit_amount) AS monthly_amount
                FROM
                  project_analytic_summary
                WHERE
                  employee_id = %s
                  AND timesheet_date = to_date(%s,'yyyy-mm-dd')
                GROUP BY
                  employee_id, timesheet_date;
            """, (line.employee_id.id, line.timesheet_date))
            line.monthly_amount = self.env.cr.fetchone()[0] or 0.0
