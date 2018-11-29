# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    phase_history = fields.Boolean(
        string='Historify when phase changes',
        help='It will historify a project each time it changes phase.')

    @api.model
    def get_values(self):
        res = super(ProjectConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        # the value of the parameter is a nonempty string
        res.update(
            phase_history=get_param('project_phase_version.phase_history',
                                    'False').lower() == 'true',
        )
        return res

    @api.multi
    def set_values(self):
        super(ProjectConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        # we store the repr of the values, since the value of the parameter is
        # a required string
        set_param('project_phase_version.phase_history',
                  repr(self.phase_history))
