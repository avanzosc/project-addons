# Copyright 2018 Maite Esnal - AvanzOSC
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# Copyright 2018 Xanti Pablo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectArea(models.Model):
    _name = 'project.area'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    type_ids = fields.One2many(comodel_name='project.area.type',
                               string='Area Types', inverse_name='area_id')
    partners = fields.Many2many(
        string="Partners", comodel_name="res.partner",
        relation="partner_area_relation", columm1="project_area_id",
        columm2='partner_id', copy=False)


class ProjectAreaType(models.Model):
    _name = 'project.area.type'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    area_id = fields.Many2one(string='Area', comodel_name='project.area')
    project_id = fields.One2many(comodel_name='project.project',
                                 inverse_name='project_area_type_id',
                                 string='Project')


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


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.onchange('project_area_id')
    def _onchange_project_area_id(self):
        self.project_area_type_id = False


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
