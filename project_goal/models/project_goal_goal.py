# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectGoalGoal(models.Model):
    _name = 'project.goal.goal'
    _description = 'Predefined Project Goals'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    type_id = fields.Many2one(
        string='Goal Type', comodel_name='project.goal.type')
