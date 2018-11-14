# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    risk_limit = fields.Float()

    @api.model
    def get_values(self):
        res = super(ProjectConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        # the value of the parameter is a nonempty string
        risk_limit = float(
            get_param('project_risk.risk_limit', '0.0'))
        res.update(
            risk_limit=risk_limit,
        )
        return res

    @api.multi
    def set_values(self):
        super(ProjectConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        # we store the repr of the values, since the value of the parameter is
        # a required string
        set_param('project_risk.risk_limit', repr(self.risk_limit))
