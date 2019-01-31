# Copyright 2018 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_location_id = fields.Many2one(
        comodel_name='res.partner', string='Location')
    participant_ids = fields.One2many(
        comodel_name='project.participant',
        inverse_name='project_id', string='Participants', copy=True)

    @api.multi
    def write(self, vals):
        res = super(ProjectProject, self).write(vals) if vals else True
        if 'active' in vals:
            # archiving/unarchiving a project does it on its participants, too
            self.with_context(active_test=False).mapped(
                'participant_ids').write(
                {'active': vals['active']})
        return res


class ProjectParticipant(models.Model):
    _name = 'project.participant'
    _description = 'Project participants'
    _rec_name = 'partner_id'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project', required=True,
        ondelete='cascade')
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Participant', required=True,
        ondelete='cascade')
    partner_user_ids = fields.One2many(
        comodel_name='res.users', string='Users',
        related='partner_id.user_ids')
    rol_id = fields.Many2one(
        comodel_name='project.participant.rol', string='Role')
    active = fields.Boolean(string='Active', default=True)


class ProjectParticipantRol(models.Model):
    _name = 'project.participant.rol'
    _description = 'Roles of project participants'

    name = fields.Char(string='Description', required=True)
