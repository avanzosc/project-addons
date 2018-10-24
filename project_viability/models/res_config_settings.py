# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from ast import literal_eval
from odoo import api, fields, models


class ProjectConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _default_viability_template(self):
        return self.env['project.viability.template'].search([], limit=1)

    enable_viability_templ = fields.Boolean(
        string='Enable Viability Template Change')
    viability_templ_id = fields.Many2one(
        comodel_name='project.viability.template',
        string='Default Viability Template',
        default=_default_viability_template)

    @api.model
    def get_values(self):
        res = super(ProjectConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        # the value of the parameter is a nonempty string
        viability_templ_id = literal_eval(
            get_param('project_viability.viability_templ_id', default='False'))
        if (viability_templ_id and
                not self.env['project.viability.template'].sudo().browse(
                    viability_templ_id).exists()):
            viability_templ_id = False
        res.update(
            enable_viability_templ=get_param(
                'project_viability.enable_viability_templ',
                'False').lower() == 'true',
            viability_templ_id=viability_templ_id,
        )
        return res

    @api.multi
    def set_values(self):
        super(ProjectConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        # we store the repr of the values, since the value of the parameter is
        # a required string
        set_param('project_viability.enable_viability_templ',
                  repr(self.enable_viability_templ))
        set_param('project_viability.viability_templ_id',
                  repr(self.viability_templ_id.id))
