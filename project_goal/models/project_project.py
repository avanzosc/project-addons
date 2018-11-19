# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    goal_ids = fields.One2many(
        comodel_name='project.goal', inverse_name='project_id', copy=True,
        context={'active_test': False})

    @api.multi
    def write(self, vals):
        res = super(ProjectProject, self).write(vals) if vals else True
        if 'active' in vals:
            # archiving/unarchiving a project does it on its goals, too
            self.with_context(active_test=False).mapped('goal_ids').write(
                {'active': vals['active']})
        return res
