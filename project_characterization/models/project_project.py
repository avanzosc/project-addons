# Copyright 2018 Maite Esnal - AvanzOSC
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectArea(models.Model):
    _name = 'project.area'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    type_id = fields.Many2one(comodel_name='project.area.type', string='Type')


class ProjectAreaType(models.Model):
    _name = 'project.area.type'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class ProjectEspaces(models.Model):
    _name = 'project.space'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class ProjectTeam(models.Model):
    _name = 'project.team'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class ProjectCharacter(models.Model):
    _name = 'project.character'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class ProjectTarget(models.Model):
    _name = 'project.target'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
