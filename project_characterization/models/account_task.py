# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class AccountTask(models.Model):
    _inherit = 'project.task.type'

    task_phase = fields.Many2one(
        comodel_name='task.phase', string='Task Phase')
    partner_ids = fields.Many2many(
        comodel_name='res.partner', string='Attendances')
    user_id = fields.Many2one(
        comodel_name='res.users', string='Responsible')


class TaskPhase(models.Model):
    _name = 'task.phase'

    name = fields.Char(string='name')
    description = fields.Char(string='description')
