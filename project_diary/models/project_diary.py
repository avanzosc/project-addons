# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectDiary(models.Model):
    _name = 'project.diary'
    _description = 'Project Diary'

    project_id = fields.Many2one(comodel_name='project.project',
                                 required=True, ondelete='cascade')
    summary = fields.Text(string='Summary')
    comments = fields.Text(string='Coordinator comments')
    active = fields.Boolean(string='Active', default=True)
