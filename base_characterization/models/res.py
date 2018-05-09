# Copyright 2018 Xanti Pablo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResCharacter(models.Model):
    _name = 'res.character'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class ResTarget(models.Model):
    _name = 'res.target'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class ResTeam(models.Model):
    _name = 'res.team'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class ResArea(models.Model):
    _name = 'res.area'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    type_ids = fields.One2many(comodel_name='res.area.type',
                               string='Area Types', inverse_name='area_id')


class ResAreaType(models.Model):
    _name = 'res.area.type'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    area_id = fields.Many2one(string='Area', comodel_name='res.area')


class ResCommittee(models.Model):
    _name = 'res.committee'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class ResStructure(models.Model):
    _name = 'res.structure'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class ResOportunitySpace(models.Model):
    _name = 'res.oportunity.space'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class ResAreaSpecialization(models.Model):
    _name = 'res.area.specialization'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

    oportunity_space_id = fields.Many2one(
        comodel_name='res.oportunity.space',
        required=True,
        string='Oportunity Spaces')


class ResActivity(models.Model):
    _name = 'res.activity'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class ResActivityType(models.Model):
    _name = 'res.activity.type'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

    activity_id = fields.Many2one(
        comodel_name='res.activity',
        required=True,
        string='Activitys')


class ResSpace(models.Model):
    _name = 'res.space'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
