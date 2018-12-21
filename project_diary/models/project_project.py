# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    diary_ids = fields.One2many(
        string='Project Diary', comodel_name='project.diary',
        inverse_name='project_id')
