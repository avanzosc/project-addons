# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    diary_ids = fields.One2many(
        string='Project Diary', comodel_name='project.diary',
        inverse_name='project_id', copy=True, context={'active_test': False})

    @api.multi
    def write(self, vals):
        res = super(ProjectProject, self).write(vals) if vals else True
        if 'active' in vals:
            # archiving/unarchiving a project does it on its diary, too
            self.with_context(active_test=False).mapped('diary_ids').write(
                {'active': vals['active']})
        return res
