# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectDiary(models.Model):
    _inherit = 'project.project'

    project_id = fields.Many2one(comodel_name='project.project')
    diary_date = fields.Datetime(string='Create_date')
    diary_user = fields.Char(string='Create_user')
    summ = fields.Text(string='Summary')
    comments = fields.Text(string='Coordinator comments')
