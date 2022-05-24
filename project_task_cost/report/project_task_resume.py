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
              project_id,
              user_id,
              SUM(planned_hours) as planned_hours,
              SUM(effective_hours) as effective_hours,
              SUM(planned_monthly_hours) as planned_monthly_hours,
              SUM(planned_cost) as planned_cost,
              SUM(effective_cost) as effective_cost,
              MIN(date_start) as date_start,
              MAX(date_end) as date_end
            FROM
              project_task
            GROUP BY
              project_id,
              user_id
        )""" % (
            self._table))
