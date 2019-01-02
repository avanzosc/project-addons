# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_smartbutton_actual_budget = fields.Boolean(
        string='Smartbutton To Current Month Budget',
        implied_group='project_budget.smartbutton_actual_budget')
    summary_line = fields.Boolean(
        string='Create a line on december 30th as summary',
        help='It will create a line on december 30th, if more than one year is'
             ' selected only for the last year.')

    @api.model
    def get_values(self):
        res = super(ProjectConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        # the value of the parameter is a nonempty string
        res.update(
            summary_line=get_param('project_budget.summary_line',
                                   'False').lower() == 'true',
        )
        return res

    @api.multi
    def set_values(self):
        super(ProjectConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        # we store the repr of the values, since the value of the parameter is
        # a required string
        set_param('project_budget.summary_line',
                  repr(self.summary_line))
