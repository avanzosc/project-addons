# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    project_area_id = fields.Many2one(
        comodel_name='project.area', string='Project Area')
    project_space_id = fields.Many2one(
        comodel_name='project.space', string='Project Space')
    project_id = fields.Many2one(
        comodel_name='project.id', string='Project Id')
    project_pe_id = fields.Many2one(
        comodel_name='project.pe',  string='Project PE')
    project_team_id = fields.Many2one(
        comodel_name='project.teams', string='Project Teams')
    project_nature_id = fields.Many2one(
        comodel_name='project.nature', string='Project Nature')
    project_sector_objetive_id = fields.Many2one(
        comodel_name='project.sector_objetive',
        string='Project Sector Objetive')
    funding_source_id = fields.Many2one(
        comodel_name='funding.source', string='Funding Source')
    department_id = fields.Many2one(
        comodel_name='hr.department', string='Internal Services Department')
    justification_deadline = fields.Date(string='Justification Deadline')
