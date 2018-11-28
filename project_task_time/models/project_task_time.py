# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectTaskTime(models.Model):
    _inherit = 'project.task'

    estim_cost = fields.Float(string='Estimated cost',
                              compute='_compute_estim_cost')
    real_hour_cost = fields.Float(string='Real hour cost',
                                  compute='_compute_real_hour_cost')
    estim_time = fields.Float(string='Estimated Hours',
                              compute='_compute_estim_time')

    @api.depends('user_id', 'planned_hours')
    def _compute_estim_cost(self):
        employee_model = self.env['hr.employee']
        for task in self.filtered('user_id'):
            employee = employee_model.search(
                [('user_id', '=', task.user_id.id)], limit=1)
            task.estim_cost = task.planned_hours * employee.timesheet_cost

    @api.depends('user_id', 'effective_hours')
    def _compute_real_hour_cost(self):
        employee_model = self.env['hr.employee']
        for task in self.filtered('user_id'):
            employee = employee_model.search(
                [('user_id', '=', task.user_id.id)], limit=1)
            task.real_hour_cost = (
                task.effective_hours * employee.timesheet_cost)

    @api.depends('user_id', 'planned_hours')
    def _compute_estim_time(self):
        return 0
