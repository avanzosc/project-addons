# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    resume_ids = fields.One2many(
        string='Resume', comodel_name='project.task.resume',
        inverse_name='project_id', readonly=True)
