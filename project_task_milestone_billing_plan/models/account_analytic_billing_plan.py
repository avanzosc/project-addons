# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class AccountAnalyticBillingPlan(models.Model):
    _inherit = 'account.analytic.billing.plan'

    project_ids = fields.One2many(
        comodel_name='project.project', string='Projects',
        related='analytic_account_id.project_ids')
    milestone_task_id = fields.Many2one(
        comodel_name='project.task', string='Milestone',
        domain="[('project_id','in',project_ids),('milestone','=',True)]")
    task_stage_id = fields.Many2one(
        comodel_name='project.task.type', string='Task Stage',
        related='milestone_task_id.stage_id', readonly=True)
