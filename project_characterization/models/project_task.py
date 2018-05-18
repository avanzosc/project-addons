# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    type_id = fields.Many2one(
        comodel_name='project.task.type2', string='Type')


class ProjectTaskType2(models.Model):
    _name = 'project.task.type2'
    _description = 'Task Type'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
