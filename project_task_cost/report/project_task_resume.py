# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import tools
from odoo import api, fields, models


class ProjectTaskResume(models.Model):
    _name = 'project.task.resume'
    _description = 'Project Task Resume'
    _auto = False
    _rec_name = 'project_id'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project')
    project_date_start = fields.Date(string='Start Date')
    project_date = fields.Date(string='Expiration Date')
    user_id = fields.Many2one(comodel_name='res.users', string='User')
    planned_hours = fields.Float(string='Initially Planned Hours')
    effective_hours = fields.Float(string='Hours Spent')
    planned_monthly_hours = fields.Float(string='Planned Monthly Hours')
    planned_cost = fields.Float(string='Estimated Cost')
    effective_cost = fields.Float(string='Real Cost')
    date_start = fields.Datetime(string='Starting Date')
    date_end = fields.Datetime(string='Ending Date')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
        CREATE or REPLACE VIEW %s as (
            SELECT
              row_number() OVER () AS id,
              task.project_id,
              MIN(project.date_start) as project_date_start,
              MAX(project.date) as project_date,
              task.user_id,
              SUM(task.planned_hours) as planned_hours,
              SUM(task.effective_hours) as effective_hours,
              SUM(task.planned_monthly_hours) as planned_monthly_hours,
              SUM(task.planned_cost) as planned_cost,
              SUM(task.effective_cost) as effective_cost,
              MIN(task.date_start) as date_start,
              MAX(task.date_end) as date_end
            FROM
              project_task as task
            INNER JOIN
              project_project as project ON task.project_id = project.id
            GROUP BY
              task.project_id,
              task.user_id
        )""" % (
            self._table))
