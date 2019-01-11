# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectClose(models.Model):
    _name = 'project.close.info'
    _description = 'Project Close Approach'
    _rec_name = 'approach'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project', required=True,
        ondelete='cascade')
    approach = fields.Char(string='Approach', translate=True)
    value = fields.Selection(
        selection=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        string='Assessment (0-5)', default=0)
    active = fields.Boolean(string='Active', default=True)
