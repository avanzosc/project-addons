# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectArea(models.Model):
    _name = 'project.area'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')


class ProjectEspaces(models.Model):
    _name = 'project.space'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')


class ProjectId(models.Model):
    _name = 'project.id'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')


class ProjectPE(models.Model):
    _name = 'project.pe'

    name = fields.Char(string='Name')
    oportunity_id = fields.Integer(string='Id')
    description = fields.Char(string='Description')


class ProjectTeams(models.Model):
    _name = 'project.teams'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')


class ProjectNature(models.Model):
    _name = 'project.nature'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')


class ProjectSectorObjetive(models.Model):
    _name = 'project.sector_objetive'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
