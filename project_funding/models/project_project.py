# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    funding_ids = fields.One2many(
        comodel_name='funding.source.project', inverse_name='project_id',
        string='Funding Sources', copy=True, context={'active_test': False})

    @api.multi
    def write(self, vals):
        res = super(ProjectProject, self).write(vals) if vals else True
        if 'active' in vals:
            # archiving/unarchiving a project does it on its funding, too
            self.with_context(active_test=False).mapped('funding_ids').write(
                {'active': vals['active']})
        return res
