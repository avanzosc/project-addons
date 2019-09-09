# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    criteria_ids = fields.One2many(
        string='Customer satisfaction', comodel_name='project.close.info',
        inverse_name='project_id',  context={'active_test': False})
    technical = fields.Selection(
        selection=[('Successful', 'Successful'),
                   ('Doubtful', 'Doubtful'),
                   ('Failed', 'Failed')], string='Technical')
    financial = fields.Selection(
        selection=[('Successful', 'Successful'),
                   ('Doubtful', 'Doubtful'),
                   ('Failed', 'Failed')], string='Financial')
    notes = fields.Text(string='Observations')

    @api.model
    def default_get(self, fields):
        rec = super(ProjectProject, self).default_get(fields)
        tmpl_lines = self.env['project.close.template'].search([])
        if tmpl_lines:
            rec.update({
                'criteria_ids': [
                    (0, 0, {'approach': x.name,
                            'active': True}) for x in tmpl_lines],
            })
        return rec

    @api.multi
    def write(self, vals):
        res = super(ProjectProject, self).write(vals) if vals else True
        if 'active' in vals:
            # archiving/unarchiving a project does it on its criteria, too
            self.with_context(active_test=False).mapped('criteria_ids').write(
                {'active': vals['active']})
        return res
