# Copyright 2018 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_location_id = fields.Many2one(
        comodel_name='res.partner', string='Location')
    participant_ids = fields.One2many(
        comodel_name='project.participant',
        inverse_name='project_id', string='Participants')


class ProjectParticipant(models.Model):
    _name = 'project.participant'
    _description = 'Project participants'
    _rec_name = 'partner_id'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project', required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Participant', required=True)
    rol_id = fields.Many2one(
        comodel_name='project.participant.rol', string='Role')


class ProjectParticipantRol(models.Model):
    _name = 'project.participant.rol'
    _description = 'Roles of project participants'

    name = fields.Char(string='Description', required=True)
