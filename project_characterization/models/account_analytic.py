# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    project_area_id = fields.Many2one(
        comodel_name='project.area', string='Area')
    project_space_id = fields.Many2one(
        comodel_name='project.space', string='Space')
    project_team_id = fields.Many2one(
        comodel_name='project.team', string='Teams')
    project_character_id = fields.Many2one(
        comodel_name='project.character', string='Character')
    project_target_id = fields.Many2one(
        comodel_name='project.target', string='Target')
    funding_source_id = fields.Many2one(
        comodel_name='funding.source', string='Funding Source')
    department_id = fields.Many2one(
        comodel_name='hr.department', string='Internal Services Department')
    justification_deadline = fields.Date(string='Justification Deadline')
    project_area_type_id = fields.Many2one(
        comodel_name='project.area.type', string='Area type',
        domain="[('area_id','=',project_area_id)]",
        ondelete='cascade')

