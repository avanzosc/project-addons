# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    def write(self, values):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        if (values.get('phase_id') and
                get_param('project_phase_version.phase_history',
                          'False').lower() == 'true'):
            for project in self.filtered(lambda p: p.phase_id.historify):
                project.button_historical()
        return super(ProjectProject, self).write(values)

    def _get_copy_data(self):
        vals = super(ProjectProject, self)._get_copy_data()
        vals.update({
            'phase_id': self.phase_id.id,
        })
        return vals


class ProjectPhase(models.Model):
    _inherit = 'project.phase'

    historify = fields.Boolean(
        string='Historify project when phase is changed.', default=True)
